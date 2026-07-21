from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import modelformset_factory
from .models import Cart, CartItem, Item, Order, OrderItem
from .forms import AddToCartForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from users.models import Profile

# Create your views here.

def index(request):
    item_list = Item.objects.all()

    context = {
        'item_list': item_list,
    }
    return render(request, 'food/index.html', context)

def item(request):
    return HttpResponse("This is an item view in the Food app.")

def details(request, item_id):
    item_info = Item.objects.get(pk=item_id)
    add_to_cart_form = AddToCartForm()

    context = {
        'item_info': item_info,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'food/detail.html', context)

@login_required(login_url='login')
def create_item(request):
    _require_manager(request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('food:index')
    else:
        form = ItemForm()

    context = {
        'form': form,
    }

    return render(request, 'food/item-form.html', context)


def _get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def _require_customer(user):
    profile = _get_profile(user)
    if profile.role != Profile.Role.CUSTOMER:
        raise PermissionDenied
    return profile


def _require_shop_owner(user):
    profile = _get_profile(user)
    if profile.role != Profile.Role.SHOP_OWNER:
        raise PermissionDenied
    return profile


def _require_manager(user):
    profile = _get_profile(user)
    if profile.role != Profile.Role.MANAGER:
        raise PermissionDenied
    return profile


@login_required(login_url='login')
def add_to_cart(request, item_id):
    _require_customer(request.user)

    if request.method != 'POST':
        return redirect('food:details', item_id=item_id)

    item = get_object_or_404(Item, pk=item_id)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item=item,
            defaults={'quantity': quantity},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return redirect('food:cart')

    return redirect('food:details', item_id=item_id)


@login_required(login_url='login')
def cart(request):
    _require_customer(request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('item')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.total_amount(),
    }
    return render(request, 'food/cart.html', context)


@login_required(login_url='login')
def update_cart_item(request, cart_item_id):
    _require_customer(request.user)
    if request.method != 'POST':
        return redirect('food:cart')

    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('food:cart')


@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    _require_customer(request.user)
    if request.method != 'POST':
        return redirect('food:cart')

    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('food:cart')


@login_required(login_url='login')
def checkout_cart(request):
    _require_customer(request.user)
    if request.method != 'POST':
        return redirect('food:cart')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('item')

    if not cart_items.exists():
        return redirect('food:cart')

    with transaction.atomic():
        order = Order.objects.create(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                unit_price=cart_item.item.item_price,
            )
        cart_items.delete()

    return redirect('food:order_detail', order_id=order.id)


@login_required(login_url='login')
def orders(request):
    profile = _get_profile(request.user)

    if profile.role == Profile.Role.SHOP_OWNER:
        order_list = Order.objects.select_related('user').prefetch_related('items__item').order_by('-created_at')
    elif profile.role == Profile.Role.CUSTOMER:
        order_list = Order.objects.filter(user=request.user).prefetch_related('items__item').order_by('-created_at')
    else:
        raise PermissionDenied

    context = {
        'order_list': order_list,
        'is_shop_owner': profile.role == Profile.Role.SHOP_OWNER,
    }
    return render(request, 'food/orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    profile = _get_profile(request.user)
    order = get_object_or_404(Order.objects.prefetch_related('items__item').select_related('user'), pk=order_id)

    if profile.role == Profile.Role.SHOP_OWNER:
        allowed = True
    else:
        allowed = order.user == request.user

    if not allowed:
        raise PermissionDenied

    context = {
        'order': order,
        'is_shop_owner': profile.role == Profile.Role.SHOP_OWNER,
        'can_customer_cancel': profile.role == Profile.Role.CUSTOMER and order.user == request.user and order.status == Order.Status.PENDING,
        'can_shop_owner_cancel': profile.role == Profile.Role.SHOP_OWNER,
        'can_shop_owner_edit': profile.role == Profile.Role.SHOP_OWNER and order.status == Order.Status.PENDING,
        'can_shop_owner_confirm': profile.role == Profile.Role.SHOP_OWNER and order.status == Order.Status.PENDING,
    }
    return render(request, 'food/order_detail.html', context)


@login_required(login_url='login')
def order_edit(request, order_id):
    _require_shop_owner(request.user)
    order = get_object_or_404(Order.objects.prefetch_related('items__item'), pk=order_id)

    if order.status != Order.Status.PENDING:
        return redirect('food:order_detail', order_id=order.id)

    OrderItemFormSet = modelformset_factory(OrderItem, fields=['quantity'], extra=0, can_delete=True)
    queryset = order.items.all()

    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            with transaction.atomic():
                instances = formset.save(commit=False)
                for deleted_object in formset.deleted_objects:
                    deleted_object.delete()
                for instance in instances:
                    instance.save()
            return redirect('food:order_detail', order_id=order.id)
    else:
        formset = OrderItemFormSet(queryset=queryset)

    context = {
        'order': order,
        'formset': formset,
    }
    return render(request, 'food/order_edit.html', context)


@login_required(login_url='login')
def confirm_order(request, order_id):
    _require_shop_owner(request.user)
    if request.method != 'POST':
        return redirect('food:order_detail', order_id=order_id)

    order = get_object_or_404(Order, pk=order_id)
    if order.status == Order.Status.PENDING:
        order.status = Order.Status.CONFIRMED
        order.confirmed_at = timezone.now()
        order.confirmed_by = request.user
        order.save(update_fields=['status', 'confirmed_at', 'confirmed_by', 'updated_at'])
    return redirect('food:order_detail', order_id=order.id)


@login_required(login_url='login')
def cancel_order(request, order_id):
    profile = _get_profile(request.user)
    if request.method != 'POST':
        return redirect('food:order_detail', order_id=order_id)

    order = get_object_or_404(Order, pk=order_id)

    if profile.role == Profile.Role.CUSTOMER:
        if order.user != request.user or order.status != Order.Status.PENDING:
            raise PermissionDenied
    elif profile.role == Profile.Role.SHOP_OWNER:
        pass
    else:
        raise PermissionDenied

    order.status = Order.Status.CANCELLED
    order.cancelled_at = timezone.now()
    order.save(update_fields=['status', 'cancelled_at', 'updated_at'])
    return redirect('food:orders')


# This is a class based view

class CreateItem(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['item_name', 'item_desc', 'item_price', 'item_image']
    template_name = 'food/item-form.html'

    def test_func(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile.role == Profile.Role.MANAGER

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

@login_required(login_url='login')
def update_item(request, id):
    _require_manager(request.user)
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'food/item-form.html', context)

@login_required(login_url='login')
def delete_item(request, id):
    _require_manager(request.user)
    item = Item.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('food:index')

    context = {
        'item': item,
    }

    return render(request, 'food/item-delete.html', context)

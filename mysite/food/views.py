from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

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

    context = {
        'item_info': item_info,
    }
    return render(request, 'food/detail.html', context)

def create_item(request):
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


# This is a class based view

class CreateItem(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['item_name', 'item_desc', 'item_price', 'item_image']
    template_name = 'food/item-form.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

def update_item(request, id):
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

def delete_item(request, id):
    item = Item.objects.get(id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('food:index')

    context = {
        'item': item,
    }

    return render(request, 'food/item-delete.html', context)

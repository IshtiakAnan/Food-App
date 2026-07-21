from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Item(models.Model):

    def __str__(self):
        return self.item_name

    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=500)
    item_price = models.IntegerField()
    item_image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def get_absolute_url(self):
        return reverse('food:details', kwargs={'item_id': self.pk})


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} cart'

    def total_amount(self):
        return sum(cart_item.line_total() for cart_item in self.items.select_related('item'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'item'], name='unique_cart_item')
        ]

    def __str__(self):
        return f'{self.quantity} x {self.item.item_name}'

    def line_total(self):
        return self.quantity * self.item.item_price


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_orders')

    def __str__(self):
        return f'Order #{self.pk} - {self.user.username}'

    def total_amount(self):
        return sum(order_item.line_total() for order_item in self.items.select_related('item'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.IntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.item.item_name} in order #{self.order_id}'

    def line_total(self):
        return self.quantity * self.unit_price
from django.contrib import admin
from .models import Cart, CartItem, Item, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'item_price', 'user_name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('cart', 'item', 'quantity')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'created_at', 'confirmed_at', 'cancelled_at')
	list_filter = ('status', 'created_at')
	inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'item', 'quantity', 'unit_price')
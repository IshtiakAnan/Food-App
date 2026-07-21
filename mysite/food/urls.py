from . import views
from django.urls import path

app_name = 'food'

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
    path('<int:item_id>/', views.details, name='details'),
    path('item/', views.item, name='item'),
    path('add/', views.CreateItem.as_view(), name='create_item'),
    path('update/<int:id>/', views.update_item, name='update_item'),
    path('delete/<int:id>/', views.delete_item, name='delete_item')
    ,path('cart/', views.cart, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout_cart, name='checkout_cart'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
]
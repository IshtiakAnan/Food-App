from . import views
from django.urls import path

app_name = 'food'

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
    path('<int:item_id>/', views.details, name='details'),
    path('item/', views.item, name='item'),
]
from . import views
from django.urls import path

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
    path('item/', views.item, name='item'),
]
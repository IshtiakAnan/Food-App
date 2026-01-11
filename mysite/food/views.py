from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, welcome to the Food app!")

def item(request):
    return HttpResponse("This is an item view in the Food app.")
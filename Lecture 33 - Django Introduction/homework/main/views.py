from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Returned By HttpResponse")

def home(request):
    return render(request, "home.html")
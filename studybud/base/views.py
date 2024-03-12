from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("home page") 


# Create your views here.
def room(request):
    return HttpResponse("ROOM page")
from django.shortcuts import render
from .models import Room



rooms = [
    {'id':1, 'name': 'learn python'},
    {'id':2, 'name': 'Java Script'},
    {'id':3, 'name': 'Front-end developers'},
]

# Create your views here.
def home(request):

    context = {'rooms': rooms}
    return render (request, 'base/home.html',context)


# Create your views here.
def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    
    context = {'room': room}
    return render (request, 'base/room.html', context)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User, Profile
from .forms import RoomForm, UserForm, ProfileForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')    

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User OR Password does not exist!')    

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


# Custom form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # Inherit existing Meta options
        model = User
        fields = ['email']  # Only include the email field

def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)    
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()        
            user.username = user.email
            user.save()    
            login(request, user)
            messages.success(request, 'Welcome! Your account registration is complete.')
            return redirect('home')
        else:
            messages.error(request, 'Something wrong')



    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_message = Message.objects.filter(Q(room__topic__name__icontains = q)).order_by('-created')
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_message': room_message}
    return render (request, 'base/home.html',context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms, 'room_message': room_message, 'topics': topics}
    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('-created')
    participants = room.participants.all()


    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'msgs':msgs, 'participants': participants}
    return render (request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)    
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        #form = RoomForm(request.POST)
        #if form.is_valid():
        #    room = form.save(commit=False)
        #    room.host = request.user
        #    room.save()
        #    return redirect('home')
        

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        #return HttpResponse('You are NOT') 
        messages.warning(request, 'You are NOT allowed to update!')
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, 'Room has been updated successfully')    
        return redirect('home')
    

    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        #return HttpResponse('You are NOT') 
        messages.error(request, 'You are NOT allowed to Delete!')
        return redirect('home')


    if request.method == 'POST':
        room.delete()
        return redirect('home')        
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk) 
    if request.user != message.user:
        messages.error(request, 'You are NOT allowed to Delete!')
        return redirect('room', pk=message.id)      

    if request.method == 'POST':
        message.delete()
        return redirect('home')


    return render(request,'base/delete.html' ,{'obj': message})

def topicsList(request):
    topics = Topic.objects.all()
    context = {'topics': topics}

    return render(request, 'base/home.html', context)

# @login_required(login_url='login')
# def userUpdate(request):
#     user = request.user
#     form = UserForm(instance=user)

#     if request.method == 'POST':
#         form = UserForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'User update successfully')
#             return redirect('user-profile', pk=user.id)

#     context = {'form': form}
#     return render(request, 'base/update_user.html', context)

@login_required(login_url='login')
def userUpdate(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user-profile', pk=user.id)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'base/update_user.html', context)


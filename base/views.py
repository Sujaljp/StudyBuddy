from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, MessageForm
from django.contrib import messages
from django.contrib.auth.models import User


# rooms= [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Machine Learning Beginners!'},
#     {'id': 3, 'name': 'Web Development Circle'},
# ]

# Create your views here.
def home(request):
    if request.GET.get('q')!=None:
        q = request.GET.get('q')
    else :
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains= q)|
        Q(description__icontains= q)
        )
    room_count = rooms.count()
    room_message = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    topic = Topic.objects.all()
    context = {'rooms':rooms, 'topic': topic , 'room_count':room_count, 'room_message':room_message}
    return render(request, 'base/index.html', context)

#User Authentication
def userLogin(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')  #.lower() function converts the value 
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def userLogout(request):
        logout(request)
        return redirect('home')

def userRegister(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
 #           user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'An error occured')
    context = { 'page':page , 'form': form }
    return render(request, 'base/login_register.html', context)

#Room related functions
@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    party = room.participants.all()
    if request.method == 'POST':
        messag = Message.objects.create(
            user= request.user,
            room= room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk= room.id)

    context = {'room':room, 'room_messages':room_messages, 
                'party' : party }
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Not Allowed')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Not Allowed')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html')

@login_required(login_url='/login')
def deleteMessage(request,pk):
    mess = Message.objects.get(id=pk)
    if request.user != mess.user:
        return HttpResponse('Not Allowed')
    if request.method == 'POST':
        mess.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':mess})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topic = Topic.objects.all()
    room_message = user.message_set.all()
    context = { 'user' : user , 'rooms': rooms, 'topic':topic , 'room_message':room_message }
    return render(request, 'base/profile.html', context)
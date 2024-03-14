from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room,Message,User

# Create your views here.
@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request,'rooms.html',{'rooms':rooms})

@login_required
def room(request,pk):
    room = Room.objects.get(pk=pk)
    messages = Message.objects.filter(room=room)[0:25]
    user=User.objects.all()

    return render(request,'room.html',{'room':room,'messages':messages,'user':user})


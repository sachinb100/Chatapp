from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SignUpForm

def frontpage(request):
    return render(request,'frontpage.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
    
        if form.is_valid():
            
            user = form.save()
        
            login(request,user)
        
            return redirect("frontpage")
        else:
            print("not valid")
    else:
        form=SignUpForm()
    
    return render(request,'signup.html',{'form':form})


    
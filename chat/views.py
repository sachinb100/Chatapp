from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .forms import SignUpForm,LoginForm
from django.contrib.auth.models import User
def frontpage(request):
    return render(request,'frontpage.html')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
    
        if form.is_valid():
            
            user = form.save()
        
            login(request,user)
            messages.success(request,'Signup Successfull')
            return redirect("frontpage")
            
        else:
            print("not valid")
    else:
        form=SignUpForm()
    
    return render(request,'signup.html',{'form':form})

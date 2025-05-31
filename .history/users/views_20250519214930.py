

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h2>Welcome to FinTrack+!</h2><a href='/users/logout/'>Logout</a>")


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')  # home page
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def home_view(request):
    return HttpResponse("<h2>Welcome to FinTrack+!</h2><a href='/users/logout/'>Logout</a>")



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # home page
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

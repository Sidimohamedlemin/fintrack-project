from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home_view(request):
    return HttpResponse("<h2>Welcome to FinTrack+!</h2><a href='/users/logout/'>Logout</a>")

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="""
        <div class="text-muted small">
            <ul style="padding-left: 18px;">
                <li>Must be at least 8 characters long</li>
                <li>Can't be too similar to your name or username</li>
                <li>Shouldn’t be a common password</li>
                <li>Must not be entirely numbers</li>
            </ul>
        </div>
        """
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form})
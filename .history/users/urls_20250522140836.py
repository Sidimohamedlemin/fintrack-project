from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', login_required(lambda request: render(request, 'users/profile.html')), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

]

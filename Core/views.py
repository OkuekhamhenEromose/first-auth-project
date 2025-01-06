from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *

# Create your views here.

@login_required
def Home(request):
    return render(request, 'index.html')

def RegisterView(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')#first_name is the one from html, like document.getElementById
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False#to validate data that has been entered


    #    To validate email and username that it isnt used by another person
        if User.objects.filter(username=username).exists():#because of User class that has been imported from .contrib#if a user fills a username that already exists
            user_data_has_error = True#it would say error that username already exists
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:#display error if length is less than 5 characters
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:#if error in any field redirect back to register page using redirect method
            return redirect('register')
        else:#once no errors, new user is created
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'register.html')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')


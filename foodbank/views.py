from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return redirect(reverse('foodbank:main_page'))
    else:
        return render(request, 'home.html', {"error_msg": "Login Failed"})
    
def logout_view(request):
    logout(request)
    return redirect(reverse('foodbank:main_page'))

def sign_up_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    user = User.objects.create_user(username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return redirect(reverse('foodbank:main_page'))

def main_page_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('foodbank:home'))

    return render(request, 'main_page.html')
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Book
from django.contrib import auth

from django.urls import reverse
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['pwd']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('myapp:index') 
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('myapp:login'))


def index(request):
    return render(request, 'myapp/index.html')

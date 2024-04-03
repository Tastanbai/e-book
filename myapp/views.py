from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login


def user_login(request):  # изменение имени представления
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)  # использование переименованной функции
                return redirect('myapp:index')  # Перенаправьте на страницу после входа
    else:
        form = LoginForm()

    return render(request, 'myapp/login.html', {'form': form})

def index(request):
    return render(request, 'myapp/index.html')


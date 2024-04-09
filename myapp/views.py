import json
from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Book
from django.contrib import auth
from django.urls import reverse
from .forms import BookForm

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


# def index(request):
#     books = Book.objects.all()
#     return render(request, 'myapp/index.html', {'books': books})

from django.db.models import Q

def index(request):
    sort = request.GET.get('sort', 'name')  # Устанавливаем 'name' как значение по умолчанию для сортировки
    search_query = request.GET.get('q', '')  # Получаем поисковый запрос

    # Получаем все книги
    books = Book.objects.all()

    # Фильтруем книги по поисковому запросу, если он предоставлен
    if search_query:
        books = books.filter(
            Q(name__icontains=search_query) | 
            Q(bbk__icontains=search_query)
        )

    # Применяем сортировку
    if sort in ['name', 'quantity', 'balance_quantity', 'bbk', 'id']:
        books = books.order_by(sort)

    return render(request, 'myapp/index.html', {'books': books, 'current_sort': sort})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('myapp:index'))
        context = {
            'form': form
        }
        return render(request, 'book/add_book.html', context=context)

    form = BookForm()

    context = {
        'form': form,
    }
    return render(request, 'myapp/add_book.html', context=context)

def edit_book(request, id):
    book_obj = Book.objects.filter(pk=id).first()
    ret = {'status': None, 'message': None}
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book_obj)
        if form.is_valid():
            form.save()
            ret['status'] = 'true'
            return HttpResponse(json.dumps(ret))
        else:
            ret['message'] = form.errors.as_text()
            return HttpResponse(json.dumps(ret))
        

    form = BookForm(instance=book_obj)

    context = {
        'form': form,
    }
    return render(request, 'myapp/edit_book.html', context=context)

def delete_book(request, id):
    Book.objects.filter(id=id).delete()
    return redirect(reverse('myapp:index'))

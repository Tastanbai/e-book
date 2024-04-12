import json
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import LoginForm, RegForm
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


from django.db.models import Q

def index(request):
    if not request.user.is_authenticated:
        return redirect('myapp:login')
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


from django.contrib.auth.models import User

def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')
            r_pwd = request.POST.get('r_pwd')
            email = request.POST.get('email')

            User.objects.create_user(
                username=name,
                password=pwd,
                email=email,
            )

            return redirect('/')
        errors = form.errors.get('__all__')

        context = {
            'form': form,
            'errors': errors
        }

        return render(request, 'myapp/reg.html', context=context)
    form = RegForm()
    context = {
        'form': form
    }

    return render(request, 'myapp/reg.html', context=context)

from .forms import PublishForm
from .models import Publish


def add_publish(request):
    if request.method == 'POST':
        form = PublishForm(request.POST)
        if form.is_valid():
            # Извлекаем книгу и запрошенное количество из данных формы
            book = form.cleaned_data['book']
            quantity_requested = form.cleaned_data['quantity']
            
            # Проверяем, достаточно ли книг в наличии
            if book.balance_quantity >= quantity_requested:
                form.save()
                return redirect(reverse('myapp:rent_book'))
            else:
                # Если запрошенное количество превышает доступное, добавляем ошибку к форме
                form.add_error('quantity', f"Только {book.balance_quantity} книг(и) доступно. Вы не можете взять {quantity_requested} книг(и).")
        
        # Если форма не валидна или есть ошибки в количестве, рендерим форму снова с ошибками
        context = {
            'form': form
        }
        return render(request, 'myapp/add_publish.html', context=context)
    
    # Для GET-запроса просто отображаем пустую форму
    else:
        form = PublishForm()
        context = {
            'form': form,
        }
        return render(request, 'myapp/add_publish.html', context=context)
    



def return_book(request, publish_id):
    # Получаем объект Publish по ID или возвращаем 404 ошибку, если такого нет
    publish = get_object_or_404(Publish, id=publish_id)
    # Удаляем объект, сигнал post_delete автоматически обновит balance_quantity
    publish.delete()
    # Перенаправляем пользователя на предыдущую страницу или главную страницу
    return redirect('myapp:rent_book')


def rent_book(request):
    # Получаем список всех записей о публикации
    publish_list = Publish.objects.all()

    # Получаем поисковой запрос из GET-параметра
    search_query = request.GET.get('q', '')

    # Фильтруем список публикаций по поисковому запросу, если он предоставлен
    if search_query:
        
        publish_list = publish_list.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(book__name__icontains=search_query)  # Исправлено на поле в связанной модели
        )

    return render(request, 'myapp/rent_book.html', {'publish_list': publish_list})

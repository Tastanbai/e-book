import json
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import LoginForm, RegForm, PublishForm, BookForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Book, Publish
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User


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


@login_required 
def index(request):
    if not request.user.is_authenticated:
        return redirect('myapp:login')
    sort = request.GET.get('sort', 'name')  # Устанавливаем 'name' как значение по умолчанию для сортировки
    search_query = request.GET.get('q', '')  # Получаем поисковый запрос

    # Получаем все книги
    #books = Book.objects.all()
    books = Book.objects.filter(user=request.user)

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



@login_required  # Убедитесь, что только аутентифицированные пользователи могут добавлять книги
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)  # Сохраняем модель, но пока не коммитим в базу данных
            book.user = request.user  # Присваиваем книге пользователя, который ее добавляет
            book.save()  # Теперь коммитим в базу данных
            return redirect(reverse('myapp:index'))  # Перенаправление на главную страницу после добавления книги
        else:
            context = {
                'form': form
            }
            return render(request, 'myapp/add_book.html', context=context)
    else:
        form = BookForm()
        context = {
            'form': form
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


def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')
            r_pwd = request.POST.get('r_pwd')
            email = request.POST.get('email')

            # Добавляем проверку на совпадение введенных паролей
            if pwd == r_pwd:
                user = User.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                )
                # Автоматический вход после регистрации
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                return redirect('myapp:index')  # Перенаправление на главную страницу после регистрации
            else:
                # Если пароли не совпадают, добавляем ошибку к форме
                form.add_error('r_pwd', 'Пароли не совпадают.')

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


@login_required
def add_publish(request):
    user_books = Book.objects.filter(user=request.user)  # Получаем список книг, принадлежащих пользователю

    if request.method == 'POST':
        form = PublishForm(request.POST)
        form.fields['book'].queryset = user_books  # Устанавливаем queryset для поля выбора книги

        if form.is_valid():
            book = form.cleaned_data['book']
            quantity_requested = form.cleaned_data['quantity']

            # Проверяем, достаточно ли книг в наличии
            if book.balance_quantity < quantity_requested:
                form.add_error('quantity', f"Только {book.balance_quantity} книг доступно.")
                return render(request, 'myapp/add_publish.html', {'form': form})

            # Сохранение публикации и обновление остатка книг
            publish_instance = form.save(commit=False)
            publish_instance.user = request.user
            book.balance_quantity -= quantity_requested
            book.save()
            publish_instance.save()
                
            return redirect(reverse('myapp:rent_book'))
        
        return render(request, 'myapp/add_publish.html', {'form': form})
    
    else:
        form = PublishForm()
        form.fields['book'].queryset = user_books  # Также устанавливаем queryset при инициализации формы
        return render(request, 'myapp/add_publish.html', {'form': form})


def return_book(request, publish_id):
    # Получаем объект Publish по ID или возвращаем 404 ошибку, если такого нет
    publish = get_object_or_404(Publish, id=publish_id)
    # Удаляем объект, сигнал post_delete автоматически обновит balance_quantity
    publish.delete()
    # Перенаправляем пользователя на предыдущую страницу или главную страницу
    return redirect('myapp:rent_book')


def rent_book(request):
    # Получаем список всех записей о публикации
    publish_list = Publish.objects.filter(user=request.user)

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

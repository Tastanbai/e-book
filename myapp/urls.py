from django.urls import path, re_path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),  
    path('logout/', views.logout, name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    re_path('edit/(\d+)/book', views.edit_book, name='edit_book'),
    re_path('delete/(\d+)/book', views.delete_book, name='delete_book'),
]
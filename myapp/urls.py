from django.urls import path,re_path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.user_login, name='login'),  
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('add_book/', views.add_book, name='add_book'),
    re_path('delete/(\d+)/book', views.delete_book, name='delete_book'),
]
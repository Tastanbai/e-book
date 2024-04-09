<<<<<<< HEAD
from django.urls import path, re_path
=======
from django.urls import path,re_path
>>>>>>> 3b13b4a057f2d51f1c03a6639e419845b1f5e539
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),  
    path('logout/', views.logout, name='logout'),
<<<<<<< HEAD
    path('add_book/', views.add_book, name='add_book'),
    re_path('edit/(\d+)/book', views.edit_book, name='edit_book'),
=======
    path('index/', views.index, name='index'),
    path('add_book/', views.add_book, name='add_book'),
>>>>>>> 3b13b4a057f2d51f1c03a6639e419845b1f5e539
    re_path('delete/(\d+)/book', views.delete_book, name='delete_book'),
]
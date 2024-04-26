from django.urls import path, re_path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('login/', views.user_login, name='login'),  
    path('', views.index, name='index'),
    path('send-email/', views.send_email, name='send_email'),
    path('rent_book/', views.rent_book, name='rent_book'),
    path('blacklist/', views.blacklist, name='blacklist'),
    path('view_returned_books/', views.view_returned_books, name='view_returned_books'),
    path('logout/', views.logout, name='logout'),
    path('reg/', views.reg, name='reg'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_publish/', views.add_publish, name='add_publish'),
    path('return_book/<int:publish_id>/', views.return_book, name='return_book'),
    re_path('edit/(\d+)/book', views.edit_book, name='edit_book'),
    re_path('delete/(\d+)/book', views.delete_book, name='delete_book'),
]
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.user_login, name='login'),  
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
]
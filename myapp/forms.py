from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    name = forms.CharField(
        min_length=6,
        label='Имя пользователя',
        error_messages={
            'required': 'Имя пользователя не может быть пустым',
            'min_length': 'Должно быть не менее 6 символов',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pwd = forms.CharField(
        min_length=6,
        label='Пароль',
        error_messages={
            'required': 'Это поле обязательно для заполнения',
            'min_length': 'Должно быть не менее 6 символов',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

from django.forms import TextInput, NumberInput
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'id', 'name', 'bbk', 'quantity', 'balance_quantity'
        )

        labels = {
            'id': 'ID',
            'name': 'Название',
            'bbk': 'ББК',
            'quantity': 'Количество',
            'balance_quantity': 'Остаток'
        }
        widgets = {
            'id': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'bbk': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'balance_quantity': NumberInput(attrs={'class': 'form-control'})
        }

        error_messages = {
            'name': {
                "required": "Название книги не может быть пустым",
                'max_length': "Название не может превышать 100 символов",
            },
            'bbk': {
                "required": "Поле ББК не может быть пустым",
            },
            'quantity': {
                "required": "Пожалуйста, укажите количество",
            },
            'balance_quantity': {
                "required": "Поле остаток не может быть пустым",
            }
        }

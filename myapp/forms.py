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

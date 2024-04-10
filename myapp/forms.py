from django import forms
from django.forms import Select, widgets

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
from .models import Book, Publish

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



from django.contrib.auth.models import User


class RegForm(forms.Form):
    name = forms.CharField(
        min_length=6,
        label='Имя пользователя',
        error_messages={
            'required': 'Имя пользователя не может быть пустым',
            'min_length': 'Не менее 6 символов',
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
            'required': 'Это поле не может быть пустым',
            'min_length': 'Не менее 6 символов',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    r_pwd = forms.CharField(
        min_length=6,
        label='Подтвердите пароль',
        error_messages={
            'required': 'Это поле не может быть пустым',
            'min_length': 'Не менее 6 символов',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label='Электронная почта',
        error_messages={'required': 'Это поле не может быть пустым', 'invalid': 'Неверный формат'},
        widget=widgets.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_name(self):
        reg_name = self.cleaned_data.get('name')
        db_name = User.objects.filter(username=reg_name)

        if not db_name:
            return reg_name
        else:
            raise forms.ValidationError('Этот пользователь уже зарегистрирован!')

    def clean_email(self):
        reg_email = self.cleaned_data.get('email')
        db_email = User.objects.filter(email=reg_email)

        if not db_email:
            return reg_email
        else:
            raise forms.ValidationError('Этот адрес электронной почты уже зарегистрирован')

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        r_pwd = self.cleaned_data.get('r_pwd')

        if pwd and r_pwd:
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise forms.ValidationError('Пароли не совпадают')


class PublishForm(forms.ModelForm):
    class Meta:
        model = Publish
        fields = (
            'name', 'city', 'email', 'phone', 'book', 'quantity'
        )

        labels = {
            'name': 'ФИО',
            'city': 'Адрес',
            'email': 'Электронная почта',
            'phone': 'Номер',
            'book': 'Книга',
            'quantity': 'Количество'
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'book': Select(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'})
        }

        error_messages = {
            'name': {
                'max_length': "Не может превышать 32 символа",
                "required": "Это поле обязательно для заполнения",
            },

            'city': {
                'max_length': ("Не может превышать 32 символа"),
                "required": "Это поле обязательно для заполнения",
            },
            'email': {
                'invalid': 'Неправильный формат адреса электронной почты',
                "required": "Это поле обязательно для заполнения",
            },
            'phone': {
                'invalid': 'Неправильный формат номера телефона',
                "required": "Это поле обязательно для заполнения",
            },
            'quantity': {
                'invalid': 'Неправильное количество',
                "required": "Это поле обязательно для заполнения",
            }
        }

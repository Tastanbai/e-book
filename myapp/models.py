from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class ReturnedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=32,null=True, verbose_name='ФИО')
    iin = models.CharField(max_length=12, verbose_name='ИИН', null=True, blank=True)
    date_out = models.DateField(null=True, blank=True, verbose_name='Дата выдачи')
    date_in = models.DateField(null=True, blank=True, verbose_name='Дата возврата')
    return_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата возврата книги')
    city = models.CharField(max_length=32, verbose_name='Адрес', null=True)
    email = models.EmailField(verbose_name='Электронная почта', null=True)
    phone = models.CharField(max_length=15,null=True, verbose_name='Номер телефона')
    book_name = models.CharField(max_length=255,null=True, verbose_name='Название книги')
    quantity = models.PositiveIntegerField(null=True, verbose_name='Количество')

    def __str__(self):
        return f"{self.book_name} returned by {self.user.username} on {self.return_date.strftime('%Y-%m-%d')}"

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ISBN=models.CharField(max_length=255, verbose_name='Книжный номер', null=True)
    author = models.CharField(max_length=255, verbose_name='Автор', null=True)
    name = models.CharField(max_length=255, verbose_name='Название книги')
    bbk = models.CharField(max_length=100, verbose_name="BBK")
    quantity = models.IntegerField(verbose_name="Количество")
    balance_quantity = models.IntegerField(verbose_name="Остаток книг")

    def __str__(self):
        return self.name

class Publish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    name = models.CharField(max_length=32, verbose_name='ФИО')
    iin = models.CharField(max_length=12, verbose_name='ИИН', null=True)
    date_out = models.DateField(null=True)
    date_in = models.DateField(null=True)
    city = models.CharField(max_length=32, verbose_name='Адрес')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, verbose_name='Номер')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name
    
    def is_overdue(self):
        """Проверяет, истекла ли дата возврата."""
        if self.date_in and self.date_in < timezone.now().date():
            return True
        return False


from django.http import Http404

# @receiver(post_save, sender=Publish)
# def update_book_balance(sender, instance, **kwargs):
#     if kwargs.get('created', True):  # Если объект Publish только что создан
#         if instance.book.balance_quantity >= instance.quantity:  # Проверяем, достаточно ли книг
#             instance.book.balance_quantity -= instance.quantity  # Вычитаем количество книг из остатка
#             instance.book.save()  # Сохраняем изменения в остатке книг
#         else:
#             # Вместо выбрасывания исключения вызываем Http404 с сообщением
#             raise Http404("Недостаточно книг в наличии")
#     else:
#         # Для редактирования существующих записей Publish
#         old_instance = Publish.objects.get(pk=instance.pk)
#         new_balance = instance.book.balance_quantity + old_instance.quantity - instance.quantity
#         if new_balance >= 0:
#             instance.book.balance_quantity = new_balance
#             instance.book.save()
#         else:
#             raise Http404("Недостаточно книг в наличии")


# @receiver(post_delete, sender=Publish)
# def restore_book_balance(sender, instance, **kwargs):
#     # Увеличиваем balance_quantity на количество возвращенных книг
#     instance.book.balance_quantity += instance.quantity
#     instance.book.save()

@receiver(post_save, sender=Publish)
def update_book_balance(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        quantity = instance.quantity
        if book.balance_quantity >= quantity:
            book.balance_quantity -= quantity
            book.save()
        else:
            raise Http404("Недостаточно книг в наличии")

@receiver(post_delete, sender=Publish)
def restore_book_balance(sender, instance, **kwargs):
    book = instance.book
    book.balance_quantity += instance.quantity
    book.save()
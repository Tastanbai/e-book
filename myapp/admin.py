from django.contrib import admin
from .models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'bbk', 'quantity', 'balance_quantity']
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

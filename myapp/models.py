from django.db import models
from django.conf import settings

class Book(models.Model):
    name = models.CharField(max_length=255)
    bbk = models.CharField(max_length=100, verbose_name="BBK")
    quantity = models.IntegerField(verbose_name="Quantity")
    balance_quantity = models.IntegerField(verbose_name="Balance Quantity")

    def __str__(self):
        return self.name


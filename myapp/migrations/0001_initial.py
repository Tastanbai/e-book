# Generated by Django 5.0.3 on 2024-04-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bbk', models.CharField(max_length=100, verbose_name='BBK')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('balance_quantity', models.IntegerField(verbose_name='Balance Quantity')),
            ],
        ),
    ]

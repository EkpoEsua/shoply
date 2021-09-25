# Generated by Django 3.2.7 on 2021-09-24 00:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price_per_kg',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_per_kg',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Price (per kg in AED)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_available',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantity (kg)'),
        ),
    ]

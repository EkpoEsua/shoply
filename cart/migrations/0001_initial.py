# Generated by Django 3.2.7 on 2021-09-23 12:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Product Name",
                        max_length=200,
                        unique=True,
                        verbose_name="Product Name",
                    ),
                ),
                (
                    "quantity_available",
                    models.IntegerField(
                        help_text="Quantity (kg)",
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Quantity (kg)",
                    ),
                ),
                (
                    "price_per_kg",
                    models.IntegerField(
                        help_text="Price (per kg in AED)",
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Price (per kg in AED)",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "purchase_quantity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("price_per_kg", models.IntegerField()),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.product"
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]

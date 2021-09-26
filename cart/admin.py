from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    """Class to fine tune admin view for Product Objects."""

    list_display = ("name", "quantity_available", "price_per_kg")


admin.site.register(Product, ProductAdmin)

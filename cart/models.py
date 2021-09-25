from typing import Collection, Optional
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _


name_text = "Product Name"
quantity_text = "Quantity (kg)"
price_text = "Price (per kg in AED)"


class Product(models.Model):
    """Class to define a Product object."""

    name = models.CharField(
        max_length=200,
        verbose_name=name_text,
        unique=True
    )

    quantity_available = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=quantity_text
    )

    price_per_kg = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=price_text
    )

    def __str__(self) -> str:
        """Return String for representing a Product object."""
        return self.name

    class Meta:
        ordering = ["id"]


class Cart(models.Model):
    """Class to represent a Cart model."""

    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    purchase_quantity = models.IntegerField(validators=[MinValueValidator(0)])

    price_per_kg = models.IntegerField(validators=[MinValueValidator(0)])
        
    class Meta:
        ordering = ["id"]
    
    def clean_fields(self, exclude: Optional[Collection[str]] = ...) -> None:
        """Ensure the price per kg field is equal to the of the product represented in the 
        product."""
        product_price_per_kg_value = self.product.price_per_kg
        cart_item_price_per_kg_value = self.price_per_kg

        if product_price_per_kg_value != cart_item_price_per_kg_value:
            raise ValidationError({
                "price_per_kg": _(
                    "Price per kg field of cart item must be equal to corresponding product."
                    # f" {product_price_per_kg_value} != {cart_item_price_per_kg_value}"
                ),
            })

        return super().clean_fields(exclude=exclude)

    



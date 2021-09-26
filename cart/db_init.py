"""Module to initialize the Database with Product and Cart records."""
from django.db.utils import OperationalError
from cart.models import Product, Cart


def initialize_database():
    """Initialze the database with Product and Cart objects."""
    potatoes, created = Product.objects.get_or_create(
        name="Potatoes", defaults={"quantity_available": 10, "price_per_kg": 5}
    )

    if created:
        potatoes_cart_item, created = Cart.objects.get_or_create(
            product=potatoes,
            defaults={"purchase_quantity": 2, "price_per_kg": potatoes.price_per_kg},
        )

        carrots, created = Product.objects.get_or_create(
            name="Carrots", defaults={"quantity_available": 6, "price_per_kg": 4}
        )

        carrots_cart_item, created = Cart.objects.get_or_create(
            product=carrots,
            defaults={"purchase_quantity": 1, "price_per_kg": carrots.price_per_kg},
        )

        onions, created = Product.objects.get_or_create(
            name="Onions", defaults={"quantity_available": 12, "price_per_kg": 2}
        )

        onions_cart_item, created = Cart.objects.get_or_create(
            product=onions,
            defaults={"purchase_quantity": 1, "price_per_kg": onions.price_per_kg},
        )


try:
    print("Initializing Database...")
    initialize_database()
except OperationalError as e:
    pass

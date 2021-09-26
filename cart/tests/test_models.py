"""Test Classes for Model Classes and functionalities."""
from django.test import TestCase
from cart.models import Product, Cart
from django.core.exceptions import ValidationError
from cart.db_init import initialize_database


class BaseModelTest(TestCase):
    """Base test for models."""

    def setUp(self) -> None:
        """Set up Database objects to be used by test."""

        # initialize new database items
        initialize_database()


class DatabaseInitializationTest(BaseModelTest):
    """Check that the database has been initialized with the expected records."""

    def test_that_potatoes_is_in_the_database(self):
        """Test that potatoes is the database with expect record."""
        potatoes = Product.objects.get(name="Potatoes")

        self.assertEqual(potatoes.name, "Potatoes")
        self.assertEqual(potatoes.quantity_available, 10)
        self.assertEqual(potatoes.price_per_kg, 5)

    def test_that_carrots_is_in_the_database(self):
        """Test that Carrot is the database with expect record."""
        carrots = Product.objects.get(name="Carrots")

        self.assertEqual(carrots.name, "Carrots")
        self.assertEqual(carrots.quantity_available, 6)
        self.assertEqual(carrots.price_per_kg, 4)

    def test_that_onions_is_in_the_database(self):
        """Test that Onions is the database with expect record."""
        onions = Product.objects.get(name="Onions")

        self.assertEqual(onions.name, "Onions")
        self.assertEqual(onions.quantity_available, 12)
        self.assertEqual(onions.price_per_kg, 2)


class ProductModelTest(BaseModelTest):
    """Test the Product Model."""

    def test_object_name_is_name_of_the_product(self):
        """Test that object name is the name of the product."""
        product = Product.objects.get(name="Potatoes")

        self.assertEqual(str(product), "Potatoes")

    def test_maximum_length_of_name_field(self):
        """Test that the maximum length of the name field is 200 characters"""
        product = Product.objects.get(pk=1)

        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_the_label_of_the_name_field(self):
        """Test the label of the name field is as expected."""
        product = Product.objects.get(pk=1)

        label = product._meta.get_field("name").verbose_name
        self.assertEqual(label, "Product Name")

    def test_the_label_of_the_quantity_available_field(self):
        """Test the label of the quantity_available field is as expected."""
        product = Product.objects.get(pk=1)

        label = product._meta.get_field("quantity_available").verbose_name
        self.assertEqual(label, "Quantity (kg)")

    def test_the_label_of_the_price_per_kg_field(self):
        """Test the label of the price_per_kg field is as expected."""
        product = Product.objects.get(pk=1)

        label = product._meta.get_field("price_per_kg").verbose_name
        self.assertEqual(label, "Price (per kg in AED)")

    def test_the_price_per_kg_and_quantity_available_fields_should_not_be_below_zero(
        self,
    ):
        """Test the value of the  price per kg field maintains the constrain of never being
        less than zero.
        """
        product = Product(name="name", quantity_available=-2, price_per_kg=-1)
        product.save()

        with self.assertRaises(ValidationError) as cm:
            product.full_clean()

        e = cm.exception
        message = e.message_dict
        expected_dict = {
            "quantity_available": ["Ensure this value is greater than or equal to 0."],
            "price_per_kg": ["Ensure this value is greater than or equal to 0."],
        }
        self.assertDictEqual(message, expected_dict)

    def test_ordering_of_items_from_database_is_by_id_in_ascending_order(self):
        """Test the items gotten from the database is ordered by id in ascending order."""
        products = Product.objects.all()

        id_count = 1
        for product in products:
            self.assertEqual(id_count, product.id)
            id_count += 1


class CartModelTest(BaseModelTest):
    """Class to define test cases for Cart model."""

    def test_ordering_of_items_from_database_is_by_id_in_ascending_order(self):
        """Test the items gotten from the database is ordered by id in ascending order."""
        cart_items = Cart.objects.all()

        id_count = 1
        for item in cart_items:
            self.assertEqual(id_count, item.id)
            id_count += 1

    def test_the_price_per_kg_and_purchase_quantity_fields_should_not_be_below_zero(
        self,
    ):
        """Test the value of the  price per kg and purchase_quantity fields maintains the
        constrain of never being less than zero.
        """
        product = Product(name="name", quantity_available=2, price_per_kg=-1)
        product.save()
        cart = Cart(product=product, purchase_quantity=-1, price_per_kg=-1)

        with self.assertRaises(ValidationError) as cm:
            cart.full_clean()

        e = cm.exception
        message = e.message_dict
        expected_dict = {
            "purchase_quantity": ["Ensure this value is greater than or equal to 0."],
            "price_per_kg": ["Ensure this value is greater than or equal to 0."],
        }
        self.assertDictEqual(message, expected_dict)

    def test_the_price_per_kg_is_same_as_that_of_the_product(self):
        """Test that the value of the price per kg field of a cart item must be equal to the
        corresponding product's value.
        """
        product = Product(name="name", quantity_available=2, price_per_kg=5)
        product.save()
        cart = Cart(product=product, purchase_quantity=2, price_per_kg=2)

        with self.assertRaises(ValidationError) as cm:
            cart.full_clean()

        e = cm.exception
        message = e.message_dict
        expected_dict = {
            "price_per_kg": [
                "Price per kg field of cart item must be equal to corresponding product."
            ]
        }
        self.assertDictEqual(message, expected_dict)

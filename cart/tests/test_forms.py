from logging import error
from cart.models import Cart, Product
from django.test import TestCase
from cart.forms import CheckOutForm, CreateItemForm, UpdateItemForm
from cart.db_init import initialize_database
from django.core.exceptions import ObjectDoesNotExist


class BaseFormTest(TestCase):
    """Base class for form tests."""

    def setUp(self) -> None:
        """Set up Database objects to be used by test."""

        # initialize new database items
        initialize_database()

    def label_test(self, form, field, expected_value):
        """Generic label test function"""
        self.assertTrue(form.fields[field].label is None 
                        or form.fields[field].label == expected_value)

    def model_field_choice_test(self, form, field, query):
        """Generic test for Model Choice Fields."""
        products = query
        products_list = products.values_list()
        choices = form.fields[field].queryset.values_list()
        self.assertEqual(list(products_list), list(choices))

class CreateItemFormTest(BaseFormTest):
    """Tests for CreateItemForm."""

    def test_price_per_kg_field_label(self):
        form = CreateItemForm()
        self.label_test(form, "price_per_kg", "Price per kg")

    def test_product_field_label(self):
        form = CreateItemForm()
        self.label_test(form, "product", "Product")

    def test_purchase_quantity_field_label(self):
        form = CreateItemForm()
        self.label_test(form, "purchase_quantity", "Purchase quantity")
    
    def test_price_per_kg_field_is_hidden(self):
        form = CreateItemForm()
        self.assertTrue(form.fields["price_per_kg"].hidden_widget)

    def test_price_per_kg_field_is_not_required(self):
        form = CreateItemForm()
        self.assertFalse(form.fields["price_per_kg"].required)

    def test_product_field_empty_value(self):
        form = CreateItemForm()
        self.assertEqual(form.fields["product"].empty_label, "Select One")

    def test_product_field_choices(self):
        form = CreateItemForm()
        self.model_field_choice_test(form, "product", Product.objects.all())

    def test_the_form_saves_model(self):
        """Test the form saves model to database."""
        # clear Cart dataase first to prevent raising Integrity error by saving duplicates.
        Cart.objects.all().delete()

        product = Product.objects.get(pk=1)
        data = {
            "product": product.id,
            "purchase_quantity": 4,
        }
        form = CreateItemForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        cart_item = form.instance
        self.assertEqual(cart_item.price_per_kg, product.price_per_kg)

    def test_error_when_saving_duplicate_item_to_cart(self):
        """Test that the form is invalid with appropraite error message and an exception is raised,
        when trying to saving
        an item already in the cart again.
        """
        product = Product.objects.get(pk=1)
        data = {
            "product": product.id,
            "purchase_quantity": 4,
        }
        form = CreateItemForm(data=data)
        self.assertTrue("Cart with this Product already exists." in form.errors["product"])
        self.assertFalse(form.is_valid())
        self.assertTrue("Item already in Cart." in form.errors["product"])
        with self.assertRaises(ValueError):
            form.save()


class UpdateItemFormTest(BaseFormTest):
    """Tests for UpdateItemForm."""

    def test_price_per_kg_field_label(self):
        form = UpdateItemForm()
        self.label_test(form, "price_per_kg", "Price per kg")

    def test_product_field_label(self):
        form = UpdateItemForm()
        self.label_test(form, "product", "Product")

    def test_purchase_quantity_field_label(self):
        form = UpdateItemForm()
        self.label_test(form, "purchase_quantity", "Purchase quantity")

    def test_model_update(self):
        """Test the form properly updates a Cart model, the purchase quantity field."""
        cart = Cart.objects.get(pk=1)
        data = {"purchase_quantity": 5}
        self.assertFalse(cart.purchase_quantity == data["purchase_quantity"])
        form = UpdateItemForm(data=data, instance=cart)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(cart.purchase_quantity == data["purchase_quantity"])


class CheckOutFormTest(BaseFormTest):
    """Tests for CheckOutForm."""

    def test_price_per_kg_field_label(self):
        form = CheckOutForm()
        self.label_test(form, "price_per_kg", "Price (per kg in AED)")

    def test_product_field_label(self):
        form = CheckOutForm()
        self.label_test(form, "product", "Product Name")

    def test_purchase_quantity_field_label(self):
        form = CheckOutForm()
        self.label_test(form, "purchase_quantity", "Quantity (kg)")

    def test_item_check_out(self):
        """Test that an item is checked out proper, with appropraite update to the Product 
        database, reducing the available quantity and Cart database, removing the item.
        """
        cart = Cart.objects.get(pk=1)
        product_id = cart.product_id
        product = Product.objects.get(pk=product_id)
        initial_quantity = product.quantity_available
        purchase_quantity = initial_quantity - 1

        # update purchase quantity to be more than
        data = {"purchase_quantity": purchase_quantity}
        update_form = UpdateItemForm(data=data, instance=cart)
        update_form.save()

        data = {
            "product":product_id,
            "purchase_quantity": purchase_quantity,
            "price_per_kg": cart.price_per_kg
        }

        check_out_form = CheckOutForm(data=data, instance=cart)
        self.assertTrue(check_out_form.is_valid())
        check_out_form.save()
        product = Product.objects.get(pk=product_id)
        self.assertEqual(product.quantity_available, 1)

        with self.assertRaises(ObjectDoesNotExist) as cm:
            cart = Cart.objects.get(pk=1)

            
    def test_purchase_quantity_more_than_available_quantity(self):
        """Test for an invalid form and corresponding error message when the purchase quantity
        of the item is more than the product's available quantity.
        """
        cart = Cart.objects.get(pk=1)
        product_id = cart.product_id
        product = Product.objects.get(pk=product_id)
        available_quantity = product.quantity_available
        purchase_quantity = available_quantity + 1

        # update purchase quantity to be more than
        data = {"purchase_quantity": purchase_quantity}
        update_form = UpdateItemForm(data=data, instance=cart)
        update_form.save()

        data = {
            "product":product_id,
            "purchase_quantity": purchase_quantity,
            "price_per_kg": product.price_per_kg
        }

        # try checking out item
        checkout_form = CheckOutForm(data=data, instance=cart)
        self.assertFalse(checkout_form.is_valid())
        error_message = f"We only have {available_quantity}kg of {product.name} left."
        self.assertTrue(error_message, checkout_form.errors.get("purchase_quantity"))

    


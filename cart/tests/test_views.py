""" Test Classes for the View Classes and functionality."""
from django.core.exceptions import ObjectDoesNotExist
from django.http import response
from cart.models import Cart, Product
from django.test import TestCase
from django.urls.base import reverse
from cart.db_init import initialize_database


class BaseViewClassTest(TestCase):
    """Base Test for view classes with common setup and functions."""

    def setUp(self) -> None:
        """Set up for the Test cases."""
        # Set up database
        initialize_database()


class CartCheckOutViewTest(BaseViewClassTest):
    """Test cases for the CartCheckOutView."""

    def test_accessability_of_view(self):
        """Test the view to ensure reachability via the name, url, and correct template is used."""
        url = reverse("cart-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, "/cart/")
        self.assertTemplateUsed(response, "cart/cart_checkout.html")

    def test_checkout_of_cart_items(self):
        """Test that items are checked out and cart is empty afterwards"""
        cart = Cart.objects.all()

        # Make request for the check out page
        url = reverse("cart-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        # Check total forms returned is equal to number of items in the cart
        self.assertEqual(form.total_form_count(), cart.count())

        # Submit the form to check out the cart
        data = {
            "form-TOTAL_FORMS": ["3"],
            "form-INITIAL_FORMS": ["3"],
            "form-MIN_NUM_FORMS": ["0"],
            "form-MAX_NUM_FORMS": ["1000"],
            "form-0-id": 1,
            "form-1-id": 2,
            "form-2-id": 3,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("checkout-success"))
        # Check that cart is emply
        self.assertEqual(Cart.objects.all().count(), 0)

    def test_checkout_success_view(self):
        """Test view displayed on sucessful checkout"""
        url = reverse("checkout-success")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, "/cart/success")
        self.assertTemplateUsed(response, "cart/checkout_success.html")

    def test_computation_of_total_cost_and_quantity_of_items_in_the_cart(self):
        """Test for correct computation of the total quantity and total cost of items in
        the cart.
        """
        url = reverse("cart-list")
        response = self.client.get(url)
        context = response.context
        self.assertEqual(context["total_quantity"], 4)
        self.assertEqual(context["total_cost"], 16)


class CartItemCreateViewTest(BaseViewClassTest):
    """Test cases for the CartItemCreateView."""

    def test_accessability_of_view(self):
        """Test the view to ensure reachability via the name, url, and correct template is used."""
        url = reverse("create-cart-item")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, "/cart/item/create/")
        self.assertTemplateUsed(response, "cart/cart_add_new_item.html")

    def test_creation_of_a_new_cart_item(self):
        """Test creation of a new cart item"""
        # Clear items from the cart
        Cart.objects.all().delete()

        # Product to use as cart item
        product = Product.objects.get(pk=1)
        product_id = product.id

        # Make request to get the form
        url = reverse("create-cart-item")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_bound)

        # Fill in form and send
        data = {
            "product": product_id,
            "purchase_quantity": 3,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cart-list"))

        # Check item in the database
        cart = Cart.objects.all()[0]
        self.assertEqual(cart.product_id, product_id)
        self.assertEqual(cart.purchase_quantity, 3)
        self.assertEqual(cart.price_per_kg, product.price_per_kg)


class CartItemUpdateViewTest(BaseViewClassTest):
    """Test case for the CartItemUpdateView."""

    def test_accessability_of_view(self):
        """Test the view to ensure reachability via the name, url, and correct template is used."""
        url = reverse("update-cart-item", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, "/cart/item/update/1")
        self.assertTemplateUsed(response, "cart/cart_form.html")

    def test_update_to_an_item_in_cart(self):
        """Test update to specified item in cart, creating the update and redirecting."""
        object_pk = 1
        cart = Cart.objects.get(pk=object_pk)
        initial_purchase_quantity = cart.purchase_quantity
        initial_item = cart.product_id
        initial_price_per_kg = cart.price_per_kg
        desired_purchase_quantity = initial_purchase_quantity + 5

        # Test form recieved with the initial get request
        url = reverse("update-cart-item", args=[object_pk])
        response = self.client.get(url)
        form = response.context["form"]
        self.assertTrue(response.status_code, 200)
        self.assertEqual(form.initial["product"], initial_item)
        self.assertEqual(form.initial["purchase_quantity"], initial_purchase_quantity)
        self.assertEqual(form.initial["price_per_kg"], initial_price_per_kg)

        # Make post request and test for an update
        data = {
            "product": initial_item,
            "purchase_quantity": desired_purchase_quantity,
            "price_per_kg": initial_price_per_kg,
        }
        response = self.client.post(url, data=data)
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, reverse("cart-list"))

        # Test for the upddate
        cart = Cart.objects.get(pk=object_pk)
        self.assertEqual(cart.product_id, initial_item)
        self.assertEqual(cart.purchase_quantity, desired_purchase_quantity)
        self.assertEqual(cart.price_per_kg, initial_price_per_kg)


class CartItemDeleteViewTest(BaseViewClassTest):
    """Test case for the CartItemDeleteView."""

    def test_accessability_of_view(self):
        """Test the view to ensure reachability via the name, url, and correct template is used."""
        url = reverse("delete-cart-item", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, "/cart/item/delete/1")
        self.assertTemplateUsed(response, "cart/cart_confirm_delete.html")

    def test_that_the_view_deletes_specified_object_in_correct_sequence(self):
        """Test objection deletion from the database, redirects back to the /cart page."""
        object_pk = 1
        cart = Cart.objects.get(pk=object_pk)

        url = reverse("delete-cart-item", args=[object_pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cart-list"))

        with self.assertRaises(ObjectDoesNotExist):
            Cart.objects.get(pk=object_pk)

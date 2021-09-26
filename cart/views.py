"""View Classes for redering pages, interacting with forms and models."""
from typing import Any, Dict
from django.forms.models import modelformset_factory
from django.http.response import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from cart.models import Cart
from cart.forms import CheckOutForm, CreateItemForm, UpdateItemForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

# Import to trigger running of the database initializations.
from cart import db_init


class CartCheckOutView(FormView):
    """Creates view for the list of items in the cart to be checked out."""

    form_class = modelformset_factory(Cart, form=CheckOutForm, extra=0)
    success_url = reverse_lazy("checkout-success")
    template_name = "cart/cart_checkout.html"

    def form_valid(self, form) -> HttpResponse:
        """Call the save method of the form to clear cart and save update to the
        Product inventory.
        """
        for f in form:
            f.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Compute the total cost and quantity of items in the cart and add it to the
        context data.
        """
        context = super().get_context_data(**kwargs)
        items = Cart.objects.all()
        total_cost = 0
        total_quantity = 0
        for item in items:
            total_cost += item.purchase_quantity * item.price_per_kg
            total_quantity += item.purchase_quantity

        context.update({"total_quantity": total_quantity, "total_cost": total_cost})

        return context


class CartItemCreateView(CreateView):
    """Creates view to add an item to the cart."""

    form_class = CreateItemForm
    template_name = "cart/cart_add_new_item.html"
    success_url = reverse_lazy("cart-list")


class CartItemUpdateView(UpdateView):
    """Creates view to edit an item in the cart."""

    form_class = UpdateItemForm
    queryset = Cart.objects.all()
    success_url = reverse_lazy("cart-list")


class CartItemDeleteView(DeleteView):
    """Creates view to delete an item from the cart."""

    model = Cart
    success_url = reverse_lazy("cart-list")

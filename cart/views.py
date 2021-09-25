from typing import Any, Dict, Optional, Type
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm, ModelForm, modelform_factory, modelformset_factory
from django.http import request
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from cart.models import Product, Cart
from cart.forms import CheckOutForm, CreateItemForm, UpdateItemForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
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
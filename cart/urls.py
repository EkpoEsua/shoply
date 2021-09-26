"""List of url routes to corresponding view Class"""
from django.urls import path
from django.views.generic.base import TemplateView
from cart import views


urlpatterns = [
    path("", views.CartCheckOutView.as_view(), name="cart-list"),
    path(
        "item/update/<int:pk>",
        views.CartItemUpdateView.as_view(),
        name="update-cart-item",
    ),
    path(
        "item/delete/<int:pk>",
        views.CartItemDeleteView.as_view(),
        name="delete-cart-item",
    ),
    path("item/create/", views.CartItemCreateView.as_view(), name="create-cart-item"),
    path(
        "success",
        TemplateView.as_view(template_name="cart/checkout_success.html"),
        name="checkout-success",
    ),
]

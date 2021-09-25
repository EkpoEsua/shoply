from django import forms
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput
from django.http.request import QueryDict
from django.utils.translation import gettext as _
from .models import Product, Cart


# labels for checkout form
price = "Price (per kg in AED)"
name = "Product Name"
quantity = "Quantity (kg)"


class CheckOutForm(forms.ModelForm):
    """Form Class for checking out of cart."""
    price_per_kg = forms.IntegerField(
        disabled=True, 
        label=price
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(), 
        disabled=True, 
        label=name
    )
    purchase_quantity = forms.IntegerField(
        disabled=True,
        label=quantity
    )

    def clean_purchase_quantity(self):
        """Ensures the purchase quantity is equal to or less than the value of quantity_available
        in corresponding Product record.
        """
        purchase_quantity = self.cleaned_data["purchase_quantity"]
        quantity_available = self.cleaned_data["product"].quantity_available
        product_name = self.cleaned_data["product"].name

        if purchase_quantity > quantity_available:
            raise ValidationError(
                _("We only have %(stock_remaining)skg of %(product_name)s left."),
                code="excess order",
                params={
                    "stock_remaining": quantity_available,
                    "product_name": product_name
                }
            )
        
        return purchase_quantity
    
    def save(self) -> None:
        """Remove item represented by this form from the cart, and update the Product
        Invetory to reflect purchase.
        """
        cart_item = self.instance
        product = cart_item.product

        # update product in the inventory 
        product.quantity_available -= cart_item.purchase_quantity
        product.save()

        #remove item from the cart
        cart_item.delete()
    
    class Meta:
        model = Cart
        fields = [
            "product", 
            "purchase_quantity", 
            "price_per_kg"
        ]

"""The Function below was mean't to filter the selection items of the CreatItemForm in the
Product field to show only items that aren't in the Cart but are in the Product table,
but somehow it doesn't seem to work as intended, because it isn't evaluated each time the 
Form is rendered, and seems to cause some error on initialization of the app, by running the
data migration."""
# def filter_items() -> QuerySet:
#     """Return a queryset of products not in the Cart."""
#     product_list = set()
#     QuerySet()
#     for product in Product.objects.all():
#         product_list.add(product.id)

#     cart_list = set()
#     for item in Cart.objects.all():
#         cart_list.add(item.product_id)
    
#     items_not_in_cart = product_list.difference(cart_list)
#     print("Kisama!!!")

#     return items_not_in_cart


class CreateItemForm(forms.ModelForm):
    """Form Class for checking out of cart."""
    price_per_kg = forms.IntegerField(required=False, widget=HiddenInput)
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Select One"
    )


    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):
        """Insert the price_per_kg value"""
        if data:
            # if the data is from a post request, do some data cleaning
            if type(data) is QueryDict:
                data = {
                    "product": int(data["product"]),
                    "purchase_quantity": int(data["purchase_quantity"]),
                }
            product_id = data["product"]
            product = Product.objects.get(pk=product_id)
            data["price_per_kg"] = product.price_per_kg

        super().__init__(data=data, files=files, auto_id=auto_id, 
                         prefix=prefix, initial=initial, error_class=error_class, 
                         label_suffix=label_suffix, empty_permitted=empty_permitted, 
                         instance=instance, use_required_attribute=use_required_attribute, 
                         renderer=renderer)
    
    def is_valid(self) -> bool:
        """Replace error on the product field with a more custom informative error."""
        valid =  super().is_valid()

        if not valid:
            if self.errors.get("product", None):
                del self.errors["product"]
                self.add_error("product", ValidationError(_("Item already in Cart.")))
        
        return valid

    class Meta:
        model = Cart
        fields = [
            "product", 
            "purchase_quantity", 
            "price_per_kg"
        ]


class UpdateItemForm(forms.ModelForm):
    """Form Class for checking out of cart."""
    price_per_kg = forms.IntegerField(disabled=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), disabled=True)

    class Meta:
        model = Cart
        fields = [
            "product", 
            "purchase_quantity", 
            "price_per_kg"
        ]

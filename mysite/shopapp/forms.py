from django import forms
from django.utils.translation import gettext_lazy as _
from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"
        labels = {
            'name': _("Name"),
            'price': _("Price"),
            'description': _("Description"),
            'discount': _("Discount"),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "product", "user", "delivery_address", "promocode"


class SCVImportForm(forms.Form):
    csv_file = forms.FileField()
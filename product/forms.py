from django import forms
from .models import *
from bin.models import BIN
from hr.models import HumanResource


class ProductTransactionForm(forms.ModelForm):
    class Meta:
        model = ProductTransaction
        exclude = ('product', 'quantity', 'stock', 'bin', 'created')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category',)


class DeliverySheetForm(forms.Form):
    delivery_man = forms.ModelChoiceField(queryset=HumanResource.objects.all(), required=False)

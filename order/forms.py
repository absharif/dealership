from django import forms
from .models import *
from bin.models import BIN
from hr.models import HumanResource
from django_select2 import forms as s2forms


class StoreWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
        # "owner_name__icontains",
        # "owner_number__icontains",
    ]


class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('date', 'bin', 'status' 'route')
        # fields = "__all__"
        widgets = {
            "outlet": StoreWidget,
        }


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('date', 'bin')
        widgets = {
            "outlet": StoreWidget,
        }


class OrderFilterForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    memo_no = forms.CharField(required=False)
    dsr = forms.ModelChoiceField(queryset=HumanResource.objects.all(), required=False) # Need to filter by BIN
    delivery_man = forms.ModelChoiceField(queryset=HumanResource.objects.all(), required=False)
    status = forms.ModelChoiceField(queryset=OrderStatus.objects.all(), required=False)


class DeliverySheetForm(forms.Form):
    delivery_man = forms.ModelChoiceField(queryset=HumanResource.objects.all(), required=False)


class PaymentFilterForm(forms.Form):
    TYPE = (
        (None, '---'),
        ('cash', 'Cash'),
        ('check', 'Check')
    )
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    token = forms.CharField(required=False)
    order = forms.IntegerField(required=False)
    type = forms.ChoiceField(choices=TYPE, required=False)
    bank_name = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)
    check_no = forms.CharField(required=False)
    check_date = forms.DateField(required=False)
    check_status = forms.ModelChoiceField(queryset=CheckStatus.objects.all(), required=False)


class NewPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('date', 'bin')
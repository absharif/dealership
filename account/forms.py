from django import forms
from .models import *
from bin.models import BIN



MONTHS = (
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )

'''
    Expense Form
'''


class ExpanseForm(forms.Form):
    date = forms.DateField()
    narration = forms.CharField(max_length=254, required=False)
    voucher = forms.CharField(max_length=254, required=False)
    source_doc = forms.ImageField(required=False)
    ledger_to = forms.ModelChoiceField(queryset=ChartOfAccount.objects.filter(chart_type='expense'))
    amount = forms.FloatField()
    ledger_from = forms.ModelChoiceField(queryset=ChartOfAccount.objects.filter(chart_type='asset', is_cash=True))


class IncomeForm(forms.Form):
    date = forms.DateField()
    voucher = forms.CharField(max_length=254, required=False)
    narration = forms.CharField(max_length=254, required=False)
    source_doc = forms.ImageField(required=False)
    ledger_from = forms.ModelChoiceField(queryset=ChartOfAccount.objects.filter(chart_type='revenue'))
    amount = forms.FloatField()
    ledger_to = forms.ModelChoiceField(queryset=ChartOfAccount.objects.filter(chart_type='asset', is_cash=True))


class DoubleEntryForm(forms.Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            bin = BIN.objects.get(id=request.session['bin'])
        except BIN.DoesNotExist:
            bin = None

        ledgers = ChartOfAccount.objects.filter(bin=bin)
        self.fields['ledger_from'] = forms.ModelChoiceField(queryset=ledgers)
        self.fields['ledger_to'] = forms.ModelChoiceField(queryset=ledgers)

    date = forms.DateField()
    voucher = forms.CharField(max_length=254, required=False)
    narration = forms.CharField(max_length=254, required=False)
    source_doc = forms.ImageField(required=False)
    amount = forms.FloatField()


class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()


class YearForm(forms.Form):
    year = forms.CharField(max_length=4)


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
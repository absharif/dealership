from django.db import models
from django.db.models.signals import post_save
from datetime import date
from bin.models import BIN
from order.models import Order

# Create your models here.


class ChartOfAccount(models.Model):
    CHART_TYPE = (
        ('dividend', 'Dividend'),
        ('expense', 'Expense'),
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
    )

    name = models.CharField(max_length=50)
    chart_type = models.CharField(max_length=10, choices=CHART_TYPE)
    balance = models.FloatField(default=0.0)
    is_cash = models.BooleanField(default=True)
    is_fund = models.BooleanField(default=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LedgerPosting(models.Model):
    date = models.DateField()
    voucher = models.CharField(max_length=15, blank=True, null=True)
    trn_type = models.CharField(max_length=15, blank=True, null=True)
    ledger = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE)
    particular = models.CharField(max_length=254, blank=True, null=True)
    narration = models.CharField(max_length=254, blank=True, null=True)
    debit_amount = models.IntegerField(default=0)
    credit_amount = models.IntegerField(default=0)
    balance = models.FloatField(default=0.0)
    source_doc = models.ImageField(upload_to='images/ledger_docs/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ledger.name) + ' : ' + str(self.narration) + ' (Dr:' + str(self.debit_amount) + ', Cr: ' + \
               str(self.credit_amount) + ', Balance: ' + str(self.balance) + ')'


def ledger_posting_post_save(sender, instance, created, *args, **kwargs):
    if created:
        ledger = instance.ledger.chart_type
        current_balance = instance.ledger.balance
        account = ChartOfAccount.objects.get(id=instance.ledger.id)

        if ledger == 'dividend' or ledger == 'expense' or ledger == 'asset':
            instance.balance = (instance.debit_amount - instance.credit_amount) + current_balance
        else:
            instance.balance = (instance.credit_amount - instance.debit_amount) + current_balance

        account.balance = instance.balance
        account.save()
        instance.save()


post_save.connect(ledger_posting_post_save, sender=LedgerPosting)


class Bank(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CheckStatus(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Payment(models.Model):
    TYPE = (
        ('cash', 'Cash'),
        ('check', 'Check')
    )

    date = models.DateField()
    token = models.CharField(max_length=10)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE, default='cash')
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)
    check_no = models.CharField(max_length=30, blank=True, null=True)
    check_date = models.DateField(blank=True, null=True)
    check_status = models.ForeignKey(CheckStatus, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField()
    remark = models.CharField(max_length=254, null=True, blank=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order.outlet) + ' : ' + str(self.amount)

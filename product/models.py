from django.db import models
from bin.models import BIN
from hr.models import HumanResource
from django.db.models.signals import post_save
from datetime import datetime


class ProductCategory(models.Model):
    name = models.CharField(max_length=120)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    mrp = models.FloatField()
    gross_price = models.FloatField()
    trade_price = models.FloatField()
    discount = models.FloatField()
    intake = models.IntegerField()
    damaged = models.IntegerField()
    free = models.IntegerField()
    stock = models.IntegerField()
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + "(" + str(self.stock) + ")"


class ProductTransaction(models.Model):
    STATUS = (
        ('intake', 'Intake'),
        ('damaged', 'Damaged')
    )

    TYPE = (
        ('in', 'IN'),
        ('out', 'OUT')
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(HumanResource, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='intake')
    transaction_type = models.CharField(max_length=10, choices=TYPE, default='in')
    stock = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=254, null=True, blank=True)
    is_company_transaction = models.BooleanField(default=False)
    created = models.DateField(null=True, blank=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE, null=True, blank=True)


def product_transaction_post_save(sender, instance, created, *args, **kwargs):
    if created:
        product = instance.product

        instance.created = datetime.today()
        instance.bin = product.bin

        if instance.transaction_type == 'in':
            instance.stock = product.stock + int(instance.quantity)
            product.stock += int(instance.quantity)

            if instance.status == 'intake':
                product.intake += int(instance.quantity)
            else:
                product.damaged += int(instance.quantity)
        else:
            instance.stock = product.stock - int(instance.quantity)
            product.stock -= int(instance.quantity)

            if instance.status == 'intake':
                product.intake -= int(instance.quantity)
            else:
                product.damaged -= int(instance.quantity)

        product.save()
        instance.save()


post_save.connect(product_transaction_post_save, sender=ProductTransaction)

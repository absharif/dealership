from django.db import models
from hr.models import HumanResource
from product.models import Product
from bin.models import BIN
from django.db.models.signals import post_save
from datetime import datetime


class Route(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=254)
    dsr = models.ForeignKey(HumanResource, on_delete=models.CASCADE, related_name='dsr')
    delivery_man = models.ForeignKey(HumanResource, on_delete=models.CASCADE, related_name='delivery_man')
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Outlet(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=254)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=120)
    owner_phone = models.CharField(max_length=11)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' [ ' + self.owner_name + ']'


class OrderStatus(models.Model):
    name = models.CharField(max_length=120)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateField(null=True, blank=True)
    memo_no = models.CharField(max_length=120)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    dsr = models.ForeignKey(HumanResource, on_delete=models.CASCADE, null=True, blank=True, related_name='dsr_sr')
    delivery_man = models.ForeignKey(HumanResource, on_delete=models.CASCADE, null=True, blank=True, related_name='delivery')
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)


def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.date = datetime.today()
        instance.bin = instance.dsr.bin
        instance.status = OrderSetting.objects.get(bin=instance.dsr.bin).default_order_status
        try:
            route = Outlet.objects.get(id=instance.outlet.id).route
        except Route.DoesNotExist():
            route = None

        if route:
            instance.route = route
        instance.save()


post_save.connect(order_post_save, sender=Order)


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product.name


def item_in_order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.bin = instance.order.bin
        instance.save()


post_save.connect(item_in_order_post_save, sender=ItemInOrder)


class OrderSetting(models.Model):
    default_order_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, null=True, blank=True)
    default_delivery_sheet_status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING,
                                                      related_name='delivery_sheet', null=True, blank=True)
    bin = models.OneToOneField(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.default_order_status.name

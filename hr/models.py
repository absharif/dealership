from django.db import models
from bin.models import BIN
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class EmployeePosition(models.Model):
    name = models.CharField(max_length=120)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HumanResource(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )
    hr_id = models.CharField(max_length=8, null=True, blank=True)
    name = models.CharField(max_length=200)
    position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=254)
    status = models.CharField(max_length=20, choices=STATUS)
    date_of_join = models.DateField(null=True, blank=True)
    date_of_resign = models.DateField(null=True, blank=True)
    bin = models.ForeignKey(BIN, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def human_resource_post_save(sender, instance, created, *args, **kwargs):
    if created:
        try:
            user = User.objects.get(username=instance.hr_id)
        except User.DoesNotExist:
            user = User.objects.create_user(
                instance.hr_id, password=instance.phone)
            user.is_superuser = False
            user.is_staff = False
            user.save()


post_save.connect(human_resource_post_save, sender=HumanResource)


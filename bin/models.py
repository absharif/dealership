from django.db import models

# Create your models here.


class BIN(models.Model):
    TYPE = (
        ('1', 'Single'),
        ('2', 'Group of Company')
    )
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=254)
    type = models.CharField(max_length=2, choices=TYPE)

    def __str__(self):
        return self.name

# Generated by Django 3.2.7 on 2022-09-03 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_bank_checkstatus_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='order.order'),
            preserve_default=False,
        ),
    ]

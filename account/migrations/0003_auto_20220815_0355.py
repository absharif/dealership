# Generated by Django 3.2.7 on 2022-08-15 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_bank_checkstatus_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='check_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='check_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.checkstatus'),
        ),
    ]

# Generated by Django 3.2.7 on 2022-08-13 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bin', '0001_initial'),
        ('order', '0003_ordersetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersetting',
            name='bin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bin.bin'),
        ),
    ]

# Generated by Django 3.2.7 on 2022-08-29 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20220812_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='free',
            field=models.IntegerField(default='0'),
            preserve_default=False,
        ),
    ]
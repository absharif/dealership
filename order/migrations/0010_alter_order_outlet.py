# Generated by Django 3.2.7 on 2022-08-31 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_outlet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='outlet',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='order.outlet'),
            preserve_default=False,
        ),
    ]

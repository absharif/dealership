# Generated by Django 3.2.7 on 2022-09-03 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bin', '0001_initial'),
        ('order', '0010_alter_order_outlet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CheckStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('token', models.CharField(max_length=10)),
                ('type', models.CharField(choices=[('cash', 'Cash'), ('check', 'Check')], default='cash', max_length=10)),
                ('check_no', models.CharField(blank=True, max_length=30, null=True)),
                ('check_date', models.DateField(blank=True, null=True)),
                ('amount', models.IntegerField()),
                ('remark', models.CharField(blank=True, max_length=254, null=True)),
                ('bank_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.bank')),
                ('bin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bin.bin')),
                ('check_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.checkstatus')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]

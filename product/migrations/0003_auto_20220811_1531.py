# Generated by Django 3.2.7 on 2022-08-11 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bin', '0001_initial'),
        ('product', '0002_auto_20220811_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttransaction',
            old_name='is_company_transection',
            new_name='is_company_transaction',
        ),
        migrations.AddField(
            model_name='producttransaction',
            name='bin',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='bin.bin'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producttransaction',
            name='status',
            field=models.CharField(choices=[('intake', 'Intake'), ('damaged', 'Damaged')], default='intake', max_length=10),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-15 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReservasWeb', '0004_auto_20180102_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_reservasweb',
            name='servicioPrestar',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.tb_product'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-08 16:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Configuracion', '0001_initial'),
        ('Caja', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_ingreso_manual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(default='', max_length=30, null=True)),
                ('monto', models.IntegerField(default='', null=True)),
                ('descripcion', models.TextField(default='', max_length=3000, null=True)),
                ('dateCreate', models.DateField(auto_now=True)),
                ('tipoIngreso', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Configuracion.tb_tipoIngreso')),
                ('tipoPago', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Configuracion.tb_formasDePago')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

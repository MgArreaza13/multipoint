# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-29 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Service', '0001_initial'),
        ('Configuracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_reservasWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTurn', models.DateField(blank=True, default='')),
                ('mail', models.EmailField(default='', max_length=30)),
                ('nombre', models.CharField(default='', max_length=30)),
                ('telefono', models.CharField(default='', max_length=30)),
                ('montoAPagar', models.IntegerField(blank=True, default=0)),
                ('montoPagado', models.IntegerField(blank=True, default=0, null=True)),
                ('isPay', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, default='Sin Descripcion', max_length=3000000)),
                ('ingenico_id', models.TextField(default='None', max_length=3000)),
                ('PagoOnline', models.BooleanField(default=False)),
                ('servicioPrestar', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Service.tb_service')),
                ('statusTurn', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Configuracion.tb_status')),
                ('turn', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='Configuracion.tb_turn_sesion')),
            ],
        ),
    ]

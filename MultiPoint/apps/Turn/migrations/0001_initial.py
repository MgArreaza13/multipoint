# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-14 13:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Service', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Client', '0001_initial'),
        ('Configuracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_turn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTurn', models.DateField(default='')),
                ('HoraTurn', models.TimeField(default='')),
                ('extraInfoTurn', models.TextField(default='', max_length=300)),
                ('isProcessClient', models.BooleanField()),
                ('isProcessCollaborator', models.BooleanField()),
                ('client', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Client.tb_client')),
                ('servicioPrestar', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Service.tb_service')),
                ('statusTurn', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Configuracion.tb_status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

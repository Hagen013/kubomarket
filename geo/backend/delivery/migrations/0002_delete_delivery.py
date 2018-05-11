# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-14 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='kladr',
        ),
        migrations.AlterField(
            model_name='pickpointcitylist',
            name='city_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID В базе службы доставки'),
        ),
        migrations.AlterField(
            model_name='sdekcitylist',
            name='city_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID В базе службы доставки'),
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]

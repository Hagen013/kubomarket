# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-06 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_cubes', '0014_productCardRecomended'),
    ]

    operations = [
        migrations.AddField(
            model_name='cubesproductcard',
            name='is_displayed_in_selections',
            field=models.BooleanField(default=False, verbose_name='Отображаемый в коллекциях'),
        ),
    ]
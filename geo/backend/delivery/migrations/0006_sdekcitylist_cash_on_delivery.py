# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_kladr_city_list_one_to_one'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdekcitylist',
            name='cash_on_delivery',
            field=models.BooleanField(default=True, verbose_name='Центр'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-06 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_orderPublicId'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order2',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=24, unique=True),
        ),
    ]

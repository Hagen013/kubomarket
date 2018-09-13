# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-08 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import yandex_money.models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_money', '0002_paymentRelations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='uuid',
            field=models.CharField(db_index=True, default=yandex_money.models.get_default_as_uuid, max_length=64, verbose_name='уникальный идентификатор'),
        ),
    ]
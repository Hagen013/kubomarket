# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-02 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_deliverypickpoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDelay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delay', models.PositiveSmallIntegerField(default=0)),
                ('product_type', models.CharField(blank=True, choices=[('', 'Не задано'), ('BACKPACK', 'BACKPACK'), ('BAG', 'BAG'), ('SUITCASE', 'SUITCASE'), ('PURSE', 'PURSE')], default='', max_length=128, verbose_name='Тип продукта')),
                ('vendor', models.CharField(blank=True, default='', max_length=128, verbose_name='Тип продукта')),
            ],
        ),
    ]

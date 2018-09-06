# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-04 13:47
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_orderDeliveryStatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order2',
            name='delivery_status',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'change_date': '', 'dispatch_number': '', 'history': [], 'service': '', 'service_status_code': None, 'state_description': '', 'status_code': None}),
        ),
        migrations.AlterField(
            model_name='order2',
            name='state',
            field=models.CharField(choices=[('новый', 'Новый'), ('недозвон', 'Недозвон'), ('доставка', 'Доставка'), ('согласован', 'Согласован'), ('выполнен', 'Выполнен'), ('отменён', 'Отменён'), ('отменён: недозвон', 'Отменён: недозвон'), ('вручен', 'вручен')], default='новый', max_length=100, verbose_name='Состояние заказа'),
        ),
    ]
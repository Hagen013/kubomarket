# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-02 14:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_paymentRelations'),
    ]

    operations = [
        migrations.AddField(
            model_name='order2',
            name='cpa',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'networks': []}),
        ),
    ]

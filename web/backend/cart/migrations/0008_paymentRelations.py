# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-08 18:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_publicId'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order2',
            name='assist_key',
        ),
        migrations.RemoveField(
            model_name='order2',
            name='assist_status',
        ),
    ]

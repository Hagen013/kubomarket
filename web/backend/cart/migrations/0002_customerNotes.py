# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-13 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order2',
            name='client_notes',
            field=models.TextField(blank=True, max_length=2000, verbose_name='Пожелания'),
        ),
    ]
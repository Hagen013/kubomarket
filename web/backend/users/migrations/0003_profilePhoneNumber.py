# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-10 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userComments'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=64, verbose_name='мобильный телефон'),
        ),
    ]
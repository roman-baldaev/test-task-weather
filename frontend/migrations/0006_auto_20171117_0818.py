# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 08:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20171115_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='name',
            new_name='city_name',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='values',
            new_name='temp_values',
        ),
    ]

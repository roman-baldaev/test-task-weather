# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_city_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='created',
            field=models.DateTimeField(),
        ),
    ]
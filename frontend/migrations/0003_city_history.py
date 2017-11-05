# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0002_delete_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.City')),
            ],
        ),
    ]

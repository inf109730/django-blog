# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoBlog', '0002_auto_20170214_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='style',
            field=models.CharField(default='Cerulean', max_length=30),
        ),
    ]

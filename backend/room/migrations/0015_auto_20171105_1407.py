# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0014_auto_20171105_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='min_time_required',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
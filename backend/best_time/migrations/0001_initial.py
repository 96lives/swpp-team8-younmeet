# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0018_auto_20171115_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='best_times', to='room.Room')),
            ],
        ),
    ]

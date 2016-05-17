# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-08 17:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160307_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 8, 17, 1, 51, 762176)),
        ),
    ]
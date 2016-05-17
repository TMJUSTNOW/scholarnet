# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20160517_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sdrive',
            name='updated',
        ),
        migrations.AddField(
            model_name='sdrive',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 15, 30, 50, 487143), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filecourse',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 15, 31, 3, 706175), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sdrive',
            name='file',
            field=models.FileField(upload_to='images/user/%Y/%m/%d'),
        ),
    ]

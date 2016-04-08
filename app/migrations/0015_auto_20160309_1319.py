# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20160309_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='url',
            field=models.ImageField(null=True, upload_to=b'images/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 9, 13, 19, 7, 747934)),
        ),
    ]

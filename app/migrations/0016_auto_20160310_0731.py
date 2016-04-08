# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20160309_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='display',
            field=models.CharField(default=datetime.datetime(2016, 3, 10, 7, 31, 47, 549361, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 7, 31, 39, 523287)),
        ),
    ]

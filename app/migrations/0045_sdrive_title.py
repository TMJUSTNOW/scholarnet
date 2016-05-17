# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_auto_20160517_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdrive',
            name='title',
            field=models.TextField(default=datetime.datetime(2016, 5, 17, 16, 7, 27, 614431)),
            preserve_default=False,
        ),
    ]

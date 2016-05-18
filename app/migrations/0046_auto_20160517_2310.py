# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_sdrive_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sdrive',
            old_name='update',
            new_name='updated',
        ),
        migrations.AddField(
            model_name='sdrive',
            name='size',
            field=models.TextField(default=datetime.datetime(2016, 5, 17, 23, 10, 7, 643520)),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20160517_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sdrive',
            old_name='update',
            new_name='updated',
        ),
    ]

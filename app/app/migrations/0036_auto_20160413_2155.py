# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_userprofile_academic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagecomments',
            name='image',
        ),
        migrations.RemoveField(
            model_name='imagecomments',
            name='user',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='year',
        ),
        migrations.DeleteModel(
            name='ImageComments',
        ),
    ]

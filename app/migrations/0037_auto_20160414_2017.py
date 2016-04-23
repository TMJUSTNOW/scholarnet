# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20160413_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='course',
            field=models.ForeignKey(to='app.Courses', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.ForeignKey(to='app.School', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='year',
            field=models.ForeignKey(to='app.Year', blank=True, null=True),
        ),
    ]

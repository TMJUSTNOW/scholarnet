# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_academicyear'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='academic',
            field=models.ForeignKey(null=True, blank=True, to='app.AcademicYear'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_subjects_academic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='academic',
            field=models.ForeignKey(blank=True, to='app.AcademicYear', null=True),
        ),
    ]

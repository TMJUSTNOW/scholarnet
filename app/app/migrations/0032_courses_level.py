# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_courselevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='level',
            field=models.ForeignKey(blank=True, null=True, to='app.CourseLevel'),
        ),
    ]

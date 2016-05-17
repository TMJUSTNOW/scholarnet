# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20160407_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_category',
            field=models.ForeignKey(blank=True, null=True, to='app.CourseCategory'),
        ),
    ]

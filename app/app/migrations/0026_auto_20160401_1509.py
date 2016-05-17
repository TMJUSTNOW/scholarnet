# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20160330_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=4)),
                ('waiting', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=b'2016-04-01 15:09:51'),
        ),
    ]

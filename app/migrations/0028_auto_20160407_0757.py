# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20160403_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Courses Categories',
                'verbose_name': 'Course Category',
            },
        ),
        migrations.AlterField(
            model_name='images',
            name='url',
            field=models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True),
        ),
    ]

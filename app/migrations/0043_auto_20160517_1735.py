# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0042_courselinker_userlinker'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileCourse',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='app.Courses')),
            ],
        ),
        migrations.CreateModel(
            name='Sdrive',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('file', models.FileField(upload_to='images/user/%Y/%m/%d')),
                ('update', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subject', models.ForeignKey(to='app.Subjects')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='filecourse',
            name='sdrive',
            field=models.ForeignKey(to='app.Sdrive'),
        ),
    ]

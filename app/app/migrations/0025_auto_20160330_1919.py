# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0024_auto_20160325_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(to='app.Courses')),
                ('school', models.ForeignKey(to='app.School')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(to='app.Year')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=b'2016-03-30 19:19:16'),
        ),
    ]

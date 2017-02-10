# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_num', models.IntegerField(default=0)),
                ('name', models.CharField(default=b'', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField()),
                ('inventory_backup', models.CharField(default=b'', max_length=1000)),
                ('teacher_id', models.CharField(default=0, max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teacher_id', models.CharField(default=b'', max_length=100)),
                ('inbox_backup', models.CharField(default=b'', max_length=1000)),
                ('spendbox_backup', models.CharField(default=b'', max_length=1000)),
                ('students', models.ManyToManyField(to='StudentApp.Student')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=500)),
                ('points', models.IntegerField(default=0)),
                ('members', models.ManyToManyField(to='StudentApp.Student')),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(to='StudentApp.Student'),
        ),
    ]

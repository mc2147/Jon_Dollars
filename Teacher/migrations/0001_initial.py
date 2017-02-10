# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodDeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.IntegerField()),
                ('name', models.CharField(max_length=1000)),
                ('id_num', models.IntegerField()),
                ('defined', models.BooleanField()),
                ('created', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_input', models.CharField(default=b'', max_length=1500)),
                ('g_deed', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('requester_id', models.IntegerField(default=0)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.BooleanField(default=False)),
                ('identifier', models.CharField(default=b'', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.IntegerField()),
                ('name', models.CharField(max_length=1000)),
                ('id_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SpendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rewardname', models.CharField(default=b'', max_length=500)),
                ('number', models.IntegerField(default=0)),
                ('username', models.CharField(default=b'', max_length=500)),
                ('studentname', models.CharField(default=b'', max_length=500)),
                ('spender', models.CharField(default=b'', max_length=500)),
            ],
        ),
    ]

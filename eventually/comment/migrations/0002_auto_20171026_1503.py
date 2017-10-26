# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='task_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='update_date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='vote_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=1024),
        ),
    ]

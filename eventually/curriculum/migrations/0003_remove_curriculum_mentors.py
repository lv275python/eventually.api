# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-15 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_added_field_goals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='mentors',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 08:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20171027_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 27, 8, 9, 22, 498900)),
        ),
    ]

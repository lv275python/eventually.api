# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-23 14:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0002_add_foreign_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

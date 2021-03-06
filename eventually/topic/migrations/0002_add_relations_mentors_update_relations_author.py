# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-13 09:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='authors',
        ),
        migrations.AddField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='mentors',
            field=models.ManyToManyField(related_name='topic_mentors', to=settings.AUTH_USER_MODEL),
        ),
    ]

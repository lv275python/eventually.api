# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 22:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_added_relations_to_owner_and_to_members'),
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='team',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='teams', to='team.Team'),
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='mentors',
            field=models.ManyToManyField(blank=True, related_name='mentors', to=settings.AUTH_USER_MODEL),
        ),
    ]

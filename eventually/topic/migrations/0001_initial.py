# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 07:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('curriculum', '0002_added_field_goals'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('curriculum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='curriculum.Curriculum')),
            ],
        ),
    ]

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django_unixdatetimefield import UnixDateTimeField
# Create your models here.

class Comment(models.Model):
    # author = models.ForeignKey('auth.user')
    text = models.TextField()
    parent_id = models.IntegerField(blank = True)
    create_date = models.DateTimeField(
        default=timezone.now)
    update_date = models.DateTimeField(
        default=timezone.now)
    event_id = models.IntegerField(blank = True)
    task_id = models.IntegerField(blank = True)
    vote_id = models.IntegerField(blank = True)

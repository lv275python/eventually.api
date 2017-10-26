from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from django_unixdatetimefield import UnixDateTimeField
# Create your models here.

class Comment(models.Model):
    '''
    
    '''

    text = models.CharField(max_length=1024)
    create_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.id,
                                 self.text,
                                 self.create_date)

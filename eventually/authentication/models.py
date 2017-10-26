from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from datetime import datetime

class customUser(AbstractBaseUser):
    #id - already exists
    first_name = models.CharField(('first name'), max_length = 20)
    second_name = models.CharField(('second name'), max_length=20)
    middle_name = models.CharField(('middle name'), max_length = 20)
    email = models.EmailField(('email address'), max_length = 40, unique = True)
    password = models.CharField(('password'), max_length = 128)
    update_date = models.DateTimeField(default = datetime.now())
    #create_date - already exists

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    objects = UserManager()

    def __str__(self):
        return self.username
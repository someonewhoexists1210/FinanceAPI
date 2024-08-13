from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

# Create your models here.
class UserManager(DefaultUserManager):
    pass

class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    objects = UserManager()

    def __str__(self):
        return self.username
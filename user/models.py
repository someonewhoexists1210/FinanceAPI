from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

# Create your models here.
class UserManager(DefaultUserManager):
    pass

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def get_transactions(self):
        return Transaction.objects.filter(models.Q(fromUser=self) | models.Q(toUser=self))
    
class Transaction(models.Model):
    fromUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    toUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.amount} - {self.date}"
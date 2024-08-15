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
    
    def transfer(self, to, amount):
        self.balance -= amount
        self.save()
        Transaction.objects.create(user=self, source=to, amount=amount)

    def recieve(self, fromUser, amount):
        self.balance += amount
        self.save()
        Transaction.objects.create(user=self, source=fromUser, amount=amount, isReciever=True)

    def get_transactions(self):
        return Transaction.objects.filter(user=self)
    
    def create_budget(self, goal, amount):
        BudgetGoal.objects.create(user=self, goal_name=goal, amount=amount)
    
    def delete_budget(self, goal):
        BudgetGoal.objects.get(user=self, goal_name=goal).delete()

    def get_budgets(self):
        return BudgetGoal.objects.filter(user=self)
    
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True)
    source = models.CharField(max_length=100, default='Unknown')
    isReciever = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'''Transaction: {str(self) if self.isReciever else self.source}{self.amount} 
        -> {self.source if self.isReciever else str(self)} --- {self.date}'''
    
    def save(self, *args, **kwargs):
        if self.user:
            self.balance = self.user.balance
        super().save(*args, **kwargs)

class BudgetGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='budget_goals')
    goal_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.goal_name + ' - ' + str(self.amount)
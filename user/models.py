from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from decimal import Decimal

# Create your models here.
class UserManager(DefaultUserManager):
    pass

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def transfer(self, to, amount, category=None):
        self.balance -= amount
        self.save()
        if category:
            category = BudgetGoal.objects.get(user=self, goal_name=category)
        Transaction.objects.create(user=self, source=to, amount=amount, category=category)

    def recieve(self, fromUser, amount):
        self.balance += amount
        self.save()
        try:
            Transaction.objects.create(user=self, source=fromUser, amount=amount, isReciever=True, category = None)
        except Exception as e:
            raise e

    def get_transactions(self):
        return Transaction.objects.filter(user=self)
    
    def create_budget(self, goal, amount):
        BudgetGoal.objects.create(user=self, goal_name=goal, amount=amount)
    
    def delete_budget(self, goal):
        BudgetGoal.objects.get(user=self, goal_name=goal).delete()

    def get_budgets(self):
        budgets = BudgetGoal.objects.filter(user=self)
        for budget in budgets:
            budget.refresh_budget()
        return BudgetGoal.objects.filter(user=self)
    
class BudgetGoal(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_refreshed = models.DateTimeField(auto_now=True, null=True)
    next_refresh = models.DateTimeField(null=True, default=timezone.now() + timedelta(days=30))

    def refresh_date(self):
        return self.last_refreshed + timedelta(days=30)
    
    def refresh_budget(self):
        if timezone.now() >= self.refresh_date():
            self.spent = 0
            self.last_refresh = timezone.now()
            self.next_refresh = self.refresh_date()
            self.save()
        
    def __str__(self):
        return self.goal_name
        
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True)
    source = models.CharField(max_length=100, default='Unknown')
    isReciever = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(BudgetGoal, on_delete=models.SET_NULL, null=True, related_name='transactions')

    def __str__(self):
        return f'''Transaction: {str(self) if self.isReciever else self.source}{self.amount} 
        -> {self.source if self.isReciever else str(self)} --- {self.date}'''
    
    def save(self, *args, **kwargs):
        if self.user:
            self.balance = self.user.balance
        if self.category and not self.isReciever:
            self.category.spent += self.amount
            self.category.save()
        super().save(*args, **kwargs)


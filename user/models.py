import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager

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
    next_refresh = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.next_refresh = self.last_refreshed + timedelta(days=30)
        super().save(*args, **kwargs)

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
        
class FinancialGoal(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.goal_name

    @property
    def progress(self):
        return (self.current_amount / self.target_amount) * 100
    
    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)
    
class RecurringTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now_add=True)
    frequency = models.CharField(max_length=50, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])
    due_date = models.DateField(null=True)
    receive = models.BooleanField(default=False)
    last_transaction = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.due_date:
            self.due_date = self.next_due(self.start_date)
        super().save(*args, **kwargs)

    def next_due(self, from_date=None):
        if not from_date:
            from_date = self.due_date
        if self.frequency == 'daily':
            return from_date + timedelta(days=1)
        elif self.frequency == 'weekly':
            return from_date + timedelta(weeks=1)
        elif self.frequency == 'monthly':
            year = from_date.year
            month = from_date.month + 1
            if month > 12:
                month = 1
                year += 1
            day = min(from_date.day, calendar.monthrange(year, month)[1])
            return datetime(year, month, day).date()
        elif self.frequency == 'yearly':
            return from_date + timedelta(days=365 if not calendar.isleap(from_date.year) else 366)
        return None
    
    def refresh(self):
        if self.due_date <= timezone.now():
            self.transaction()
    
    def transaction(self):
        if self.receive:
            self.user.recieve(self.description, self.amount)
        else:
            self.user.transfer(self.description, self.amount)
        self.start_date = self.due_date
        self.last_transaction = timezone.now()
        self.save()
    
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True)
    source = models.CharField(max_length=100, default='Unknown')
    isReciever = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(BudgetGoal, on_delete=models.CASCADE, null=True, related_name='transactions')
    recurring = models.ForeignKey(RecurringTransaction, on_delete=models.CASCADE, null=True, blank=True)

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

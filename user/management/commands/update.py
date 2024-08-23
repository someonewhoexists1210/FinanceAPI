from django.core.management.base import BaseCommand
from django.utils import timezone
from user.models import BudgetGoal, RecurringTransaction

class Command(BaseCommand):
    help = 'Updates recurring transactions'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        transactions = RecurringTransaction.objects.all()
        budgets = BudgetGoal.objects.all()
        for transaction in transactions:
            transaction.refresh()
        for budget in budgets:
            budget.refresh_budget()
        self.stdout.write(self.style.SUCCESS('Successfully updated recurring transactions and budgets'))

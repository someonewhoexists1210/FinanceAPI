from django.contrib import admin
from .models import RecurringTransaction, Transaction

class RecurringTransactionAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        print(f"Deleting RecurringTransaction: {obj}")
        transactions = Transaction.objects.filter(recurring=obj)
        print(f"Transactions to update: {transactions}")
        transactions.update(recurring=None)
        super().delete_model(request, obj)        
        print(f"RecurringTransaction {obj} deleted")
        
admin.site.register(RecurringTransaction, RecurringTransactionAdmin)
admin.site.register(Transaction)
from decimal import Decimal
import json
from django.http import HttpResponse
from user.models import CustomUser, BudgetGoal, Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required(login_url='/log/')
def index(request):
    return render(request, 'balance.html', {'balance': request.user.balance})

@login_required(login_url='/log/')
def transaction(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        isReciever = request.POST['recieving'] == '1'

        if amount <= 0:
            return HttpResponse('Invalid amount')

        try:
            if isReciever:
                request.user.recieve(request.POST.get('source', 'Unknown'), amount)
            else:
                if amount > request.user.balance:
                    return HttpResponse('Insufficient balance')
                if not request.POST['category'] or request.POST['category'] == 'None':
                    cat = None
                else:
                    cat = request.POST['category']
                request.user.transfer(request.POST.get('source', 'Unknown'), amount, cat)
        except Exception as e:
            return HttpResponse(str(e))

    transactions = request.user.get_transactions()
    return render(request, 'transaction.html', {'transactions': transactions})


@login_required(login_url='/log/')
def budget(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        goal_name = request.POST['goal_name']
        if amount <= 0:
            return HttpResponse('Invalid amount')
        request.user.create_budget(goal_name, amount)

    budgets = request.user.get_budgets().values('id', 'goal_name', 'amount', 'spent', 'date_created', 'next_refresh')
    budgets_json = json.dumps(list(budgets), default=str)
    return render(request, 'budget.html', {'budgets': list(budgets), 'budgets_json': budgets_json})

@login_required(login_url='/log/')
def delete_transaction(request, id):
    transaction = request.user.get_transactions().get(id=id)
    transaction.delete()
    return redirect('/transaction/')

@login_required(login_url='/log/')
def delete_budget(request, id):
    budget = request.user.get_budgets().get(id=id)
    budget.delete()
    return redirect('/budget/')
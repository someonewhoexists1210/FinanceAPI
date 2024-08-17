from decimal import Decimal
import json
from django.http import HttpResponse
from user.models import FinancialGoal, BudgetGoal, Transaction
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
        print(request.POST['category'])

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

    transactions = Transaction.objects.filter(user=request.user)
    categories = BudgetGoal.objects.filter(user=request.user).values('goal_name')
    return render(request, 'transaction.html', {'transactions': transactions, 'categories': categories})

@login_required(login_url='/log/')
def budget(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        goal_name = request.POST['goal_name']
        if amount <= 0:
            return HttpResponse('Invalid amount')
        BudgetGoal.objects.create(user=request.user, goal_name=goal_name, amount=amount)

    budgets = request.user.get_budgets().values('id', 'goal_name', 'amount', 'spent', 'date_created', 'next_refresh')
    budgets_json = json.dumps(list(budgets), default=str)
    return render(request, 'budget.html', {'budgets': list(budgets), 'budgets_json': budgets_json})

@login_required(login_url='/log/')
def delete_transaction(request, id):
    Transaction.objects.get(id=id).delete()
    return redirect('/transaction/')

@login_required(login_url='/log/')
def delete_budget(request, id):
    BudgetGoal.objects.get(user=request.user, id=id).delete()
    return redirect('/budget/')

@login_required(login_url='/log/')
def finance_goals(request):
    if request.method == 'POST':
        target_amount = Decimal(request.POST['amount'])
        goal_name = request.POST['goal_name']
        due_date = request.POST['due_date']
        if target_amount <= 0:
            return HttpResponse('Invalid amount')
        FinancialGoal.objects.create(user=request.user, goal_name=goal_name, target_amount=target_amount, due_date=due_date)
    finance_goals = FinancialGoal.objects.filter(user=request.user)
    return render(request, 'finance.html', {'goals': finance_goals})

@login_required(login_url='/log/')
def save(request, id=None):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        goal = FinancialGoal.objects.get(id=id)
        if goal.current_amount + amount > goal.target_amount:
            return render(request, 'save.html', {'goals': FinancialGoal.objects.filter(user=request.user), 'completed': goal.id})
        goal.current_amount += amount  
        request.user.balance -= amount
        request.user.save()
        goal.save()     
        return redirect('/finance-goals/')
    return render(request, 'save.html', {'goals': FinancialGoal.objects.filter(user=request.user)})

@login_required(login_url='/log/')
def delete_goal(request, id):
    FinancialGoal.objects.get(id=id).delete()
    return redirect('/finance-goals/')
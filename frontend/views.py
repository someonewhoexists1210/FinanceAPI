from decimal import Decimal

from django.http import HttpResponse
from user.models import CustomUser as User
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
                request.user.transfer(request.POST.get('source', 'Unknown'), amount)
        except Exception as e:
            return HttpResponse(str(e))

    transactions = request.user.get_transactions()
    return render(request, 'transaction.html', {'transactions': transactions})

@login_required(login_url='/log/')
def delete_transaction(request, id):
    transaction = request.user.get_transactions().get(id=id)
    transaction.delete()
    return redirect('/transaction/')
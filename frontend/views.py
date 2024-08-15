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
        fromUser = request.POST.get('fromUser')
        toUser = request.POST.get('toUser')
        amount = Decimal(request.POST.get('amount'))

        if fromUser != request.user.username and toUser != request.user.username:
            return HttpResponse('Can\'t transfer to self', status=400)
        
        try:
            fromUser = User.objects.get(username=fromUser)
        except User.DoesNotExist:
            return HttpResponse('From User not found', status=404)
        try:
            toUser = User.objects.get(username=toUser)
        except User.DoesNotExist:
            return HttpResponse('To User not found', status=404)
        
        # if fromUser.balance < amount:
        #     return HttpResponse(fromUser.username + ' has insufficient funds ' + fromUser.password, status=400)
        #     return HttpResponse('Insufficient funds', status=400)
        
        fromUser.transfer(toUser, amount)    
    transactions = request.user.get_transactions()
    return render(request, 'transaction.html', {'transactions': transactions})
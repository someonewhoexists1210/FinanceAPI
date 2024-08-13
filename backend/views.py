import json
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from django.shortcuts import render

# Create your views here.
def transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount'))
            user = request.user
            user.balance += amount
            user.save()

            return JsonResponse({'balance': user.balance}, status=200)
        except Exception as e:
            print(e)
            return HttpResponse('Transaction failed', status=400)
def balance(request):
    return JsonResponse({'balance': request.user.balance})
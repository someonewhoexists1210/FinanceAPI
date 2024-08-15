import json
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from django.shortcuts import render

# Create your views here.
def transaction(request):
    transactions = request.user.get_transactions()
    return render(request, 'transaction.html', {'transactions': transactions})
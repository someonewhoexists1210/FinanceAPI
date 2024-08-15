from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import requests

@login_required(login_url='/log/')
def index(request):
    return render(request, 'balance.html', {'balance': request.user.balance})

def transaction(request):
    return redirect('http://localhost:8000/back/transaction/')
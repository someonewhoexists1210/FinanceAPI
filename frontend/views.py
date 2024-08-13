from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return redirect('login')

def home(request):
    return redirect('/back/balance')

def transaction(request):
    return render(request, 'transaction.html')
from django.urls import path
from . import views

urlpatterns = [
    path('transaction/', views.transaction, name='transaction'),
    path('balance/', views.balance, name='balance'),
]
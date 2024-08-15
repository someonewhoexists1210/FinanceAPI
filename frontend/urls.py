from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('transaction/', views.transaction, name='transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('transaction/', views.transaction, name='transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('delete-budget/<int:id>/', views.delete_budget, name='delete_budget'),
    path('budget/', views.budget, name='budget'),
    path('finance-goals/', views.finance_goals, name='finance_goals'),
    path('save/<int:id>/', views.save, name='save_post'),
    path('save/', views.save, name='save'),
    path('delete_goal/<int:id>/', views.delete_goal, name='delete_goal'),
    path('recurring/', views.get_recurring, name='recurring'),
    path('delete_recurring/<int:id>/', views.delete_recurring, name='delete_recurring'),
]
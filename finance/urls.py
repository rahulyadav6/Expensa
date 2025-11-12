from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('', views.DashboardView, name='dashboard'),
    path('transaction/add/', views.TransactionCreateView, name='transaction_add'),
    path('transactions/', views.TransactionListView, name='transaction_list'),
    path('goal/add/', views.GoalCreateView, name='goal_add'),
]
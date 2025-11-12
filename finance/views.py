from django.shortcuts import render, redirect
from finance.forms import RegisterForm, TransactionForm
from django.contrib.auth import login
from django.views import View


# class RegisterView(View):
#     def get(self, request, *args, **kwargs):
#         form = RegisterForm()
#         return render(request, 'finance/register.html', {'form': form})
#     def get(self, request, *args, **kwargs):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             redirect('')

# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'finance/dashboard.html')

# class TransactionCreateView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'finance/transaction_form.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, TransactionForm, GoalForm
from django.contrib.auth.decorators import login_required
from .models import Transaction, Goal 

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = RegisterForm()
        return render(request, 'finance/register.html', {'form': form})

@login_required
def DashboardView(request):
    return render(request, 'finance/dashboard.html')


@login_required
def TransactionCreateView(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard') 
    else:
        form = TransactionForm()
        return render(request, 'finance/transaction_form.html', {'form': form})

@login_required
def TransactionListView(request):
    transactions = Transaction.objects.all()
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})


@login_required
def GoalCreateView(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
        return render(request, 'finance/goal_form.html', {'form': form})
         
    else:
        form = GoalForm()
        return render(request, 'finance/goal_form.html', {'form': form})

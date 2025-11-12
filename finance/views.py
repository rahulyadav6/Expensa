

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

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login
from .forms import RegisterForm, TransactionForm, GoalForm
from django.contrib.auth.decorators import login_required
from .models import Transaction, Goal
from django.db.models import Sum 
from django.views import View
from .admin import TransactionResource
from django.contrib import messages


def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard') 
    else:
        form = RegisterForm()
        return render(request, 'finance/register.html', {'form': form})

@login_required
def DashboardView(request):
    transactions = Transaction.objects.filter(user = request.user)
    goals = Goal.objects.filter(user = request.user)
    
    # Calculate total income and expenses
    total_expense = Transaction.objects.filter(user = request.user, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = Transaction.objects.filter(user = request.user, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0

    net_savings = total_income - total_expense
    remaining_savnigs = net_savings
    goal_progress = []
    for goal in goals:
        if remaining_savnigs >= goal.target_amount:
            goal_progress.append({'goal': goal, 'progress': 100})
            remaining_savnigs -= goal.target_amount
        elif remaining_savnigs > 0:
            progress = (remaining_savnigs / goal.target_amount) * 100
            goal_progress.append({'goal': goal, 'progress': progress})
            remaining_savnigs = 0
        else:
            goal_progress.append({'goal': goal, 'progress': 0})

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings' : net_savings,
        'goal_progress': goal_progress,
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def TransactionCreateView(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard') 
    else:
        form = TransactionForm()
        return render(request, 'finance/transaction_form.html', {'form': form})

@login_required
def TransactionListView(request):
    transactions = Transaction.objects.filter(user = request.user)
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})


@login_required
def GoalCreateView(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('dashboard')
        return render(request, 'finance/goal_form.html', {'form': form})
         
    else:
        form = GoalForm()
        return render(request, 'finance/goal_form.html', {'form': form})

def export_transaction(request):
    user_transaction = Transaction.objects.filter(user = request.user)
    transaction_resource = TransactionResource()
    dataset = transaction_resource.export(queryset=user_transaction)
    excel_data = dataset.export('xlsx')
    # create an HttpResponse with the correct MIME type for an Excel file
    response = HttpResponse(excel_data, content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # set the header for downloading the file 
    response['Content-Disposition'] = 'attachment; filename = transactions_report.xlsx'
    return response
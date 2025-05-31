from django.shortcuts import render, redirect
from .models import Income, Expense, Budget
from .forms import IncomeForm, ExpenseForm, BudgetForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import calendar
from datetime import datetime



from django.contrib import messages

@login_required
def dashboard(request):
    now = datetime.now()
    current_month = now.strftime('%B')
    
    incomes = Income.objects.filter(user=request.user, date__month=now.month)
    expenses = Expense.objects.filter(user=request.user, date__month=now.month)
    budget = Budget.objects.filter(user=request.user, month=current_month).first()

    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    balance = total_income - total_expense

    percent_used = None
    over_budget = False
    if budget:
        percent_used = (total_expense / budget.limit) * 100
        if total_expense > budget.limit:
            over_budget = True
            messages.warning(request, f"⚠️ You have exceeded your budget for {current_month}!")

    return render(request, 'finance/dashboard.html', {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'budget': budget,
        'percent_used': percent_used,
        'over_budget': over_budget,
    })


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'finance/add_budget.html', {'form': form})

@login_required
def chart_data(request):
    now = datetime.now()
    expenses = Expense.objects.filter(user=request.user, date__month=now.month)
    category_totals = {}

    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    return JsonResponse(category_totals)


from django.shortcuts import render, redirect
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    balance = total_income - total_expense
    return render(request, 'finance/dashboard.html', {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
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

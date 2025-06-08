from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import calendar
from django.db.models import Sum
from .models import Income, Expense, Budget
from .forms import IncomeForm, ExpenseForm, BudgetForm
@login_required
from django.shortcuts import render
from .models import Transaction, Budget
from datetime import datetime
import calendar

def dashboard_view(request):
    month_str = request.GET.get('month', datetime.now().strftime('%B'))
    month_number = list(calendar.month_name).index(month_str)
    transaction_type = request.GET.get('type', 'All')

    transactions = Transaction.objects.filter(date__month=month_number)

    if transaction_type != 'All':
        transactions = transactions.filter(type=transaction_type)

    total_income = sum(t.amount for t in transactions if t.type == 'Income')
    total_expense = sum(t.amount for t in transactions if t.type == 'Expense')

    try:
        budget = Budget.objects.latest('created_at')  # or filter by user if needed
        budget_left = budget.limit - total_expense
    except Budget.DoesNotExist:
        budget = None
        budget_left = None

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'budget': budget,
        'budget_left': budget_left,
        'selected_month': month_str,
        'selected_type': transaction_type,
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, f"✅ Income of ${income.amount} added.")
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {
        'form': form,
        'title': 'Add Income',
    })


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
    return render(request, 'finance/add_expense.html', {
        'form': form,
        'title': 'Add Expense',
    })


@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.month = datetime.now().strftime('%B')
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'finance/add_budget.html', {
        'form': form,
        'title': 'Add Budget',
    })



@login_required
def chart_data(request):
    month_param = request.GET.get('month')
    now_time = datetime.now()
    try:
        month_number = list(calendar.month_name).index(month_param) if month_param else now_time.month
    except ValueError:
        month_number = now_time.month

    expenses = Expense.objects.filter(user=request.user, date__month=month_number)
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + float(expense.amount)

    return JsonResponse(category_totals)



@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finance/edit_expense.html', {
        'form': form,
        'title': 'Edit Expense',
    })


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'finance/delete_expense.html', {
        'expense': expense
    })


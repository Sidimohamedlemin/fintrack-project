from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import calendar
from .models import Income, Expense, Budget
from .forms import IncomeForm, ExpenseForm, BudgetForm
from django.shortcuts import get_object_or_404  


@login_required
def dashboard(request):
    month_param = request.GET.get('month')
    type_param = request.GET.get('type')
    now = datetime.now()

    if month_param:
        try:
            month_number = list(calendar.month_name).index(month_param)
        except ValueError:
            month_number = now.month
    else:
        month_number = now.month

    # Start with all filtered by user + month
    incomes = Income.objects.filter(user=request.user, date__month=month_number)
    expenses = Expense.objects.filter(user=request.user, date__month=month_number)

    # Apply type filter
    if type_param == 'income':
        expenses = []  # hide expenses
    elif type_param == 'expense':
        incomes = []  # hide incomes

    # Calculate totals and balance
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    balance = total_income - total_expense

    current_month_name = calendar.month_name[month_number]
    budget = Budget.objects.filter(user=request.user, month=current_month_name).first()

    percent_used = None
    if budget and budget.limit:
        percent_used = (total_expense / budget.limit) * 100
        if total_expense > budget.limit:
            messages.warning(request, f"⚠️ You have exceeded your budget for {current_month_name}!")

    month_list = list(calendar.month_name)[1:]

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'budget': budget,
        'percent_used': percent_used,
        'month_list': month_list,
    }

    return render(request, 'finance/dashboard.html', context)
    monthly_data = []
    for i in range(1, 13):
        income_sum = Income.objects.filter(user=request.user, date__month=i).aggregate(total=Sum('amount'))['total'] or 0
        expense_sum = Expense.objects.filter(user=request.user, date__month=i).aggregate(total=Sum('amount'))['total'] or 0
        monthly_data.append({
            'month': calendar.month_abbr[i],
            'income': float(income_sum),
            'expense': float(expense_sum),
        })

    context.update({
        'monthly_data': monthly_data,
    })
    return render(request, 'finance/dashboard.html', context)
    
    # Filter incomes and expenses for the selected month and current user
    incomes = Income.objects.filter(user=request.user, date__month=month_number)
    expenses = Expense.objects.filter(user=request.user, date__month=month_number)
    
    # Calculate totals and balance
    total_income = sum(i.amount for i in incomes)
    total_expense = sum(e.amount for e in expenses)
    balance = total_income - total_expense
    
    # Get the month name from the number
    current_month_name = calendar.month_name[month_number]
    
    # Get budget for that month, if any
    budget = Budget.objects.filter(user=request.user, month=current_month_name).first()
    percent_used = None
    if budget and budget.limit:
        percent_used = (total_expense / budget.limit) * 100
        if total_expense > budget.limit:
            messages.warning(request, f"⚠️ You have exceeded your budget for {current_month_name}!")
    month_list = list(calendar.month_name)[1:]
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'budget': budget,
        'percent_used': percent_used,
        'month_list': month_list,
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
        'title': 'Income',
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
    return render(request, 'finance/add_budget.html', {
        'form': form,
        'title': 'Monthly Budget',
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
    return render(request, 'finance/add_budget.html', {'form': form})


@login_required
def chart_data(request):
    # Filter expenses by month similar to dashboard view
    month_param = request.GET.get('month')
    now = datetime.now()
    if month_param:
        try:
            month_number = list(calendar.month_name).index(month_param)
        except ValueError:
            month_number = now.month
    else:
        month_number = now.month
    expenses = Expense.objects.filter(user=request.user, date__month=month_number)
    category_totals = {}
    for expense in expenses:
        # Convert amount to float to ensure JSON serializability
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
    return render(request, 'finance/edit_expense.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'finance/delete_expense.html', {'expense': expense})

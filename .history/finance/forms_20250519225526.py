# finance/forms.py
from django import forms
from .models import Income, Expense, Budget

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date']
 

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'limit']

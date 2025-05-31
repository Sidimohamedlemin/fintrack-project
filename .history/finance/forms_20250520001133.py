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
        fields = ['amount', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'limit']



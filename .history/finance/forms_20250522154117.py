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



class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=(
            "<ul class='text-muted small'>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>It can't be entirely numeric.</li>"
            "<li>It can't be too similar to your other personal information.</li>"
            "<li>It can't be a commonly used password.</li>"
            "</ul>"
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
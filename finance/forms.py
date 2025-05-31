# finance/forms.py
from django import forms
from .models import Income, Expense, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        widget=forms.PasswordInput,
        help_text="""
        <div class="text-muted small">
            <ul style="padding-left: 18px;">
                <li>Must be at least 8 characters long</li>
                <li>Can't be too similar to your name or username</li>
                <li>Shouldn’t be a common password</li>
                <li>Must not be entirely numbers</li>
            </ul>
        </div>
        """
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

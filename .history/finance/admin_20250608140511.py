from django.contrib import admin
from .models import Transaction
from .models import Income, Expense, Budget

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Transaction)

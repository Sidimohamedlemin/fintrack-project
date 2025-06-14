from django.contrib import admin
from .models import Income, Expense, Budget, Transaction

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'label', 'amount', 'date')

admin.site.register(Transaction, TransactionAdmin) 
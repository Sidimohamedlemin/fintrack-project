from django.contrib import admin
from .models import Transaction
from .models import Income, Expense, Budget

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Transaction)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'amount', 'category', 'date']
    list_filter = ['type', 'date']
    search_fields = ['category', 'notes']
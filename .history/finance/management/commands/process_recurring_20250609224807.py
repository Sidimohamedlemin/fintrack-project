from django.core.management.base import BaseCommand
from finance.models import RecurringTransaction, Income, Expense
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Process recurring transactions and generate corresponding Income/Expense records'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        recurring_transactions = RecurringTransaction.objects.filter(next_run__lte=today)

        for r in recurring_transactions:
            if r.type == 'income':
                Income.objects.create(
                    user=r.user,
                    amount=r.amount,
                    source=r.category_or_source,
                    notes=r.notes,
                    date=today
                )
            elif r.type == 'expense':
                Expense.objects.create(
                    user=r.user,
                    amount=r.amount,
                    category=r.category_or_source,
                    description=r.notes,
                    date=today
                )

            # Calculate next_run
            if r.repeat == 'daily':
                r.next_run += timedelta(days=1)
            elif r.repeat == 'weekly':
                r.next_run += timedelta(weeks=1)
            elif r.repeat == 'monthly':
                r.next_run = r.next_run.replace(month=r.next_run.month + 1 if r.next_run.month < 12 else 1,
                                                year=r.next_run.year + 1 if r.next_run.month == 12 else r.next_run.year)
            r.save()

        self.stdout.write(self.style.SUCCESS('✅ Recurring transactions processed.'))

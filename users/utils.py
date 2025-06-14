from datetime import timedelta, date
from finance.models import Transaction  
from .models import RecurringTransaction

def process_recurring_transactions():
    today = date.today()
    for rec in RecurringTransaction.objects.all():
        if not rec.last_processed:
            rec.last_processed = rec.start_date - timedelta(days=1)

        next_date = rec.last_processed
        while True:
            if rec.frequency == 'daily':
                next_date += timedelta(days=1)
            elif rec.frequency == 'weekly':
                next_date += timedelta(weeks=1)
            elif rec.frequency == 'monthly':
                # Handle month skipping
                month = (next_date.month % 12) + 1
                year = next_date.year + (next_date.month // 12)
                day = min(next_date.day, 28)  # avoid 31st issues
                next_date = date(year, month, day)

            if next_date > today:
                break

            # Create new transaction
            Transaction.objects.create(
                user=rec.user,
                type=rec.type,
                amount=rec.amount,
                category_or_source=rec.category,
                notes=rec.notes,
                date=next_date
            )

            rec.last_processed = next_date
            rec.save()

from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User
from .models import Budget, Expense
from django.db.models import Sum

def check_budget_alerts():
    current_month = now().strftime('%B')
    users = User.objects.all()

    for user in users:
        budget = Budget.objects.filter(user=user, month=current_month).first()
        if not budget:
            continue

        total_expense = Expense.objects.filter(user=user, date__month=now().month).aggregate(
            total=Sum('amount')
        )['total'] or 0

        usage_percent = (total_expense / budget.limit) * 100 if budget.limit > 0 else 0

        if usage_percent >= 80:
            send_mail(
                subject='🚨 FinTrack+ Budget Alert',
                message=f"Hi {user.username},\n\nYou've spent {usage_percent:.2f}% of your {current_month} budget!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

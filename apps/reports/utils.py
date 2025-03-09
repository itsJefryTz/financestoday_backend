from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from apps.income.models import Income
from apps.expense.models import Expense
from .models import Report

def generate_reports(user):
    # Error handling.
    try:
        # Create reports from the first income or expense.
        oldest_income = Income.objects.all().order_by('date').first()
        oldest_expense = Expense.objects.all().order_by('date').first()
        
        # Check if there are income and expenses.
        if oldest_income is not None and oldest_expense is not None:
            oldest_date = min(oldest_income.date, oldest_expense.date)
        elif oldest_income is not None:
            oldest_date = oldest_income.date
        elif oldest_expense is not None:
            oldest_date = oldest_expense.date
        else:
            oldest_date = None
            
        if oldest_date is not None:
            # Create reports from the oldest date to today.
            today = timezone.now().date()
            current_date = oldest_date
            while current_date <= today:
                first_icome = Income.objects.filter(user=user, date=current_date).first()
                first_expense = Expense.objects.filter(user=user, date=current_date).first()
                # If either of the two exists.
                if first_icome or first_expense:
                    daily_income = Income.objects.filter(user=user, date=current_date).aggregate(total=Sum('amount'))['total'] or 0
                    daily_expense = Expense.objects.filter(user=user, date=current_date).aggregate(total=Sum('amount'))['total'] or 0
                    daily_balance = daily_income - daily_expense
                    # Check if a report from that date already exists.
                    report = Report.objects.filter(user=user, start_date=current_date).first()
                    if report:
                        report.type = 'Diario'
                        report.start_date=current_date
                        report.end_date=current_date
                        report.income = daily_income
                        report.expense = daily_expense
                        report.balance = daily_balance
                        report.save()
                    else:
                        Report.objects.create(
                            user=user, type='Diario',
                            start_date=current_date, end_date=current_date, income=daily_income, 
                            expense=daily_expense, balance=daily_balance)
                current_date += timedelta(days=1)
    except Exception as e:
        print(f'ERROR: {e}')
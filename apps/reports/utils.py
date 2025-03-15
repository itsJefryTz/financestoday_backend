from django.utils import timezone
from datetime import timedelta, date, datetime
from django.db.models import Sum, Max, Min

from apps.income.models import Income
from apps.expense.models import Expense
from .models import Report

def oldest_income_or_expense(user):
    # Error handling.
    try:
        oldest_income = Income.objects.filter(user=user).order_by('date').first()
        oldest_expense = Expense.objects.filter(user=user).order_by('date').first()
        
        if oldest_income is not None and oldest_expense is not None:
            oldest_date = min(oldest_income.date, oldest_expense.date)
        elif oldest_income is not None:
            oldest_date = oldest_income.date
        elif oldest_expense is not None:
            oldest_date = oldest_expense.date
        else:
            oldest_date = None
        return oldest_date
    
    except Exception as e:
        print(f'An error has occurred: {e}')
        
def recent_income_or_expense(user):
    # Error handling.
    try:
        recent_income = Income.objects.filter(user=user).order_by('-date').first()
        recent_expense = Expense.objects.filter(user=user).order_by('-date').first()
        
        if recent_income is not None and recent_expense is not None:
            recent_date = max(recent_income.date, recent_expense.date)
        elif recent_income is not None:
            recent_date = recent_income.date
        elif recent_expense is not None:
            recent_date = recent_expense.date
        else:
            recent_date = None
        return recent_date
    
    except Exception as e:
        print(f'An error has occurred: {e}')
        
def generate_daily_reports(user):
    try:
        oldest_date = oldest_income_or_expense(user)
        most_recent_date = recent_income_or_expense(user)
            
        if oldest_date is not None:
            if most_recent_date is None:
                most_recent_date = timezone.now().date()
            
            # Create daily reports.
            current_date = oldest_date
            while current_date <= most_recent_date:
                daily_income = Income.objects.filter(user=user, date=current_date).aggregate(total=Sum('amount'))['total'] or 0
                daily_expense = Expense.objects.filter(user=user, date=current_date).aggregate(total=Sum('amount'))['total'] or 0
                daily_balance = daily_income - daily_expense
                
                report = Report.objects.filter(user=user, type='Diario', start_date=current_date).first()
                if report:
                    report.type = 'Diario'
                    report.start_date = current_date
                    report.end_date = current_date
                    report.income = daily_income
                    report.expense = daily_expense
                    report.balance = daily_balance
                    report.save()
                else:
                    Report.objects.create(
                        user=user,
                        type='Diario',
                        start_date=current_date,
                        end_date=current_date,
                        income=daily_income, 
                        expense=daily_expense,
                        balance=daily_balance)
                current_date += timedelta(days=1)
                
    except Exception as e:
        print(f'An error has occurred: {e}')
        
def generate_weekly_reports(user):
    try:
        oldest_date = oldest_income_or_expense(user)
        most_recent_date = recent_income_or_expense(user)
        
        if oldest_date is not None:
            if most_recent_date is None:
                most_recent_date = timezone.now().date()
        
            # Create weekly reports.
            current_date = oldest_date
            while current_date <= most_recent_date:
                week_start = current_date - timedelta(days=current_date.weekday()) # Lunes de esa semana.
                week_end = week_start + timedelta(days=6) # Domingo de esa semana.
                
                weekly_income = Income.objects.filter(user=user, date__range=(week_start, week_end)).aggregate(total=Sum('amount'))['total'] or 0
                weekly_expense = Expense.objects.filter(user=user, date__range=(week_start, week_end)).aggregate(total=Sum('amount'))['total'] or 0
                weekly_balance = weekly_income - weekly_expense
                
                report = Report.objects.filter(user=user, type='Semanal', start_date=week_start).first()
                if report:
                    report.type = 'Semanal'
                    report.start_date = week_start
                    report.end_date = week_end
                    report.income = weekly_income
                    report.expense = weekly_expense
                    report.balance = weekly_balance
                    report.save()
                else:
                    Report.objects.create(
                        user=user,
                        type='Semanal',
                        start_date=week_start,
                        end_date=week_end,
                        income=weekly_income, 
                        expense=weekly_expense,
                        balance=weekly_balance)
                current_date += timedelta(days=7)
                
    except Exception as e:
        print(f'An error has occurred: {e}')
        
def generate_monthly_reports(user):
    try:
        oldest_date = oldest_income_or_expense(user)
        most_recent_date = recent_income_or_expense(user)

        if oldest_date and most_recent_date:
            start_year = oldest_date.year
            end_year = most_recent_date.year

            for year in range(start_year, end_year + 1):
                start_of_year = datetime(year, 1, 1)
                end_of_year = datetime(year, 12, 31)

                current_date = start_of_year
                while current_date <= end_of_year:
                    month_start = current_date.replace(day=1)
                    next_month = month_start.month + 1 if month_start.month < 12 else 1
                    month_end = (month_start.replace(month=next_month, day=1) - timedelta(days=1)) if next_month != 1 else month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
                    
                    monthly_income = Income.objects.filter(user=user, date__range=(month_start, month_end)).aggregate(total=Sum('amount'))['total'] or 0
                    monthly_expense = Expense.objects.filter(user=user, date__range=(month_start, month_end)).aggregate(total=Sum('amount'))['total'] or 0
                    monthly_balance = monthly_income - monthly_expense
                    
                    report = Report.objects.filter(user=user, type='Mensual', start_date=month_start).first()
                    if report:
                        report.type = 'Mensual'
                        report.start_date = month_start
                        report.end_date = month_end
                        report.income = monthly_income
                        report.expense = monthly_expense
                        report.balance = monthly_balance
                        report.save()
                    else:
                        Report.objects.create(
                            user=user,
                            type='Mensual',
                            start_date=month_start,
                            end_date=month_end,
                            income=monthly_income, 
                            expense=monthly_expense,
                            balance=monthly_balance)

                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1, day=1)
                
    except Exception as e:
        print(f'An error has occurred: {e}')
        
def generate_annual_reports(user):
    try:
        oldest_date = oldest_income_or_expense(user)
        most_recent_date = recent_income_or_expense(user)

        current_year = oldest_date.year
        while current_year <= most_recent_date.year:
            year_start = date(current_year, 1, 1)
            year_end = date(current_year, 12, 31)

            annual_income = Income.objects.filter(user=user, date__range=(year_start, year_end)).aggregate(total=Sum('amount'))['total'] or 0
            annual_expense = Expense.objects.filter(user=user, date__range=(year_start, year_end)).aggregate(total=Sum('amount'))['total'] or 0
            annual_balance = annual_income - annual_expense

            report = Report.objects.filter(user=user, type='Anual', start_date=year_start).first()
            if report:
                report.type = 'Anual'
                report.start_date = year_start
                report.end_date = year_end
                report.income = annual_income
                report.expense = annual_expense
                report.balance = annual_balance
                report.save()
            else:
                Report.objects.create(
                    user=user,
                    type='Anual',
                    start_date=year_start,
                    end_date=year_end,
                    income=annual_income, 
                    expense=annual_expense,
                    balance=annual_balance)
            current_year += 1
                
    except Exception as e:
        print(f'An error has occurred: {e}')

def generate_reports(user):
    # Error handling.
    try:
        generate_daily_reports(user)
        generate_weekly_reports(user)
        generate_monthly_reports(user)
        generate_annual_reports(user)
        pass
    except Exception as e:
        print(f'An error has occurred: {e}')
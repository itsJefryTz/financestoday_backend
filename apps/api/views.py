from django.db.models import Sum, Max
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from apps.income.models import Income
from apps.income.serializers import IncomeSerializer
from apps.expense.models import Expense
from apps.expense.serializers import ExpenseSerializer
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer
from apps.reports.utils import generate_reports

# Create your views here.
class UserDashboardData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # --------- Card data ---------.
        now = timezone.now()
        total_income_this_month = Income.objects.filter(user=request.user, date__year=now.year, date__month=now.month).aggregate(total=Sum('amount'))['total'] or 0
        total_expenses_this_month = Expense.objects.filter(user=request.user, date__year=now.year, date__month=now.month).aggregate(total=Sum('amount'))['total'] or 0
        # ------ Chart and tables -----.
        latest_income_date = Income.objects.filter(user=request.user).aggregate(Max('date'))['date__max']
        latest_expense_date = Expense.objects.filter(user=request.user).aggregate(Max('date'))['date__max']
        latest_date = max(latest_income_date, latest_expense_date)
        latest_date_year = latest_date.year
        generate_reports(request.user)
        monthly_reports = Report.objects.filter(user=request.user, type='Mensual', start_date__year=latest_date_year).order_by('start_date')
        serialized_reports = ReportSerializer(monthly_reports, many=True).data
        return Response({
            'message': '¡Estás autenticado!',
            'card_data': {
                'total_income_this_month': total_income_this_month,
                'total_expenses_this_month': total_expenses_this_month},
            'chart_and_tables': {
                'monthly_reports': serialized_reports},
        }, status=status.HTTP_200_OK)

class UserCategoriesList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        categories = Category.objects.filter(user=user).order_by('-created_at')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserIncomeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        incomes = Income.objects.filter(user=user).order_by('-date')
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserExpenseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        expense = Expense.objects.filter(user=user).order_by('-date')
        serializer = ExpenseSerializer(expense, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserReportsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        generate_reports(user)
        reports = Report.objects.filter(user=user).order_by('-start_date')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
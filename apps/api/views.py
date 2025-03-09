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
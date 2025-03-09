from django.urls import path

from .views import UserCategoriesList, UserIncomeList, UserExpenseList, UserReportsList

urlpatterns = [
    path('v1/user_categories_list/', UserCategoriesList.as_view(), name='user_categories_list'),
    path('v1/user_income_list/', UserIncomeList.as_view(), name='user_income_list'),
    path('v1/user_expense_list/', UserExpenseList.as_view(), name='user_expense_list'),
    path('v1/user_reports_list/', UserReportsList.as_view(), name='user_report_list'),
]
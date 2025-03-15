from rest_framework import serializers

from apps.categories.serializers import CategorySerializer

from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Expense
        fields = '__all__'
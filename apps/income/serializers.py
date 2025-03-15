from rest_framework import serializers

from apps.categories.serializers import CategorySerializer

from .models import Income

class IncomeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Income
        fields = '__all__'
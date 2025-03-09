from django.contrib import admin
from django import forms

from .models import Expense

# Register your models here.
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        self.fields['category'].queryset = self.fields['category'].queryset.filter(type='Gasto')
        
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'user', 'category', 'name', 'amount', 'date', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'amount', 'date', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'amount', 'date')
    list_filter = ('user', 'date', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date',)
admin.site.register(Expense, ExpenseAdmin)
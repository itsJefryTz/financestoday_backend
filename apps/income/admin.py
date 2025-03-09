from django.contrib import admin
from django import forms

from .models import Income

# Register your models here.
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        
        self.fields['category'].queryset = self.fields['category'].queryset.filter(type='Ingreso')

class IncomeAdmin(admin.ModelAdmin):
    form = IncomeForm
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'user', 'category', 'name', 'amount', 'date', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'amount', 'date', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'date')
    list_filter = ('user', 'date', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date',)
admin.site.register(Income, IncomeAdmin)
from django.contrib import admin
from django import forms

from .models import Report

# Register your models here.
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ('user',)
        
class ReportAdmin(admin.ModelAdmin):
    form = ReportForm
    
    def get_queryset(self, request):        
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'type', 'start_date', 'end_date', 'income', 'expense', 'balance', 'created_at', 'updated_at')
    list_display_links = ('id', 'type', 'start_date', 'end_date', 'income', 'expense', 'balance', 'created_at', 'updated_at')
    search_fields = ('id', 'type', 'income', 'expense', 'balance')
    list_filter = ('type', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-start_date',)
admin.site.register(Report, ReportAdmin)
from django.contrib import admin
from django import forms

from .models import Income

# Register your models here.
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude = ('user',)

class IncomeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['category'].queryset = form.base_fields['category'].queryset.filter(user=request.user, type='Ingreso')
        return form
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request, obj)
        return obj.user == request.user
    
    form = IncomeForm
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'category', 'name', 'amount', 'date', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', 'amount', 'date', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'date')
    list_filter = ('date', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date',)
admin.site.register(Income, IncomeAdmin)
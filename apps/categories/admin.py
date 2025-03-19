from django.contrib import admin
from django import forms

from .models import Category

# Register your models here.
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('user',)

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
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
    
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'type', 'name', 'description', 'created_at', 'updated_at')
    list_display_links = ('id', 'type', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'type', 'description')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 10
admin.site.register(Category, CategoryAdmin)
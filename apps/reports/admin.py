from django.contrib import admin

from .models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'user', 'type', 'start_date', 'end_date', 'income', 'expense', 'balance', 'created_at', 'updated_at')
    list_display_links = ('id', 'user', 'type', 'start_date', 'end_date', 'income', 'expense', 'balance', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'type', 'income', 'expense', 'balance')
    list_filter = ('user__username', 'type', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-start_date',)
admin.site.register(Report, ReportAdmin)
from django.contrib import admin

from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'user', 'type', 'name', 'description', 'created_at', 'updated_at')
    list_display_links = ('id', 'type', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'type', 'description')
    list_filter = ('user', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 10
admin.site.register(Category, CategoryAdmin)
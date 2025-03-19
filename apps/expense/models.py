from django.db import models
from django.contrib.auth.models import User

from apps.categories.models import Category

# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='expense_user', verbose_name='Usuario')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expense_category', verbose_name='Categoría')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    date = models.DateField(verbose_name='Fecha')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ('-date',)
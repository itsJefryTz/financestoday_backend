from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_user', verbose_name='Usuario')
    type = models.CharField(max_length=100, choices=[('Diario', 'Diario'), ('Semanal', 'Semanal'),
                                                     ('Mensual', 'Mensual'), ('Anual', 'Anual')], verbose_name='Tipo')
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin')
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ingresos')
    expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gastos')
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Balance')
    description = models.TextField(blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-created_at']
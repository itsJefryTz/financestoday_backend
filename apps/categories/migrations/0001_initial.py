# Generated by Django 5.1.6 on 2025-03-08 23:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_user', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['-created_at'],
            },
        ),
    ]

# departments/admin.py

from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department')  # Removed created_at and updated_at
    list_filter = ('head_of_department',)         # Removed created_at
    search_fields = ('name', 'head_of_department__username', 'description')  # Adjusted as necessary

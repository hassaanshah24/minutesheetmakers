# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserForm

class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Extends Django's UserAdmin with custom fields.
    """
    model = CustomUser
    form = CustomUserForm  # Use the custom form for add/edit actions
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

    fieldsets = (
        ('Account Info', {
            'fields': ('username', 'password', 'email', 'phone_number', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        ('New User Creation', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'role', 'password',
                       'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

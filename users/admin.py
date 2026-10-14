from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'codeforces_handle', 'is_handle_verified', 'is_staff', 'date_joined')
    list_filter = ('is_handle_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'codeforces_handle')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Competitive Programming', {
            'fields': ('codeforces_handle', 'is_handle_verified')
        }),
    )
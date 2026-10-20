from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'github_username', 'created_at']
    search_fields = ['user__username', 'location', 'github_username']
    list_filter = ['created_at']

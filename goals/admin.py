from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'goal_type', 'target_value', 'current_value', 'is_completed', 'deadline']
    list_filter = ['goal_type', 'is_completed']
    search_fields = ['user__username', 'title']

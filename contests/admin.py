from django.contrib import admin
from .models import Contest


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest_name', 'contest_id', 'rank', 'old_rating', 'new_rating', 'rating_update_time')
    list_filter = ('rating_update_time',)
    search_fields = ('contest_name', 'user__username', 'contest_id')
    ordering = ('-rating_update_time',)
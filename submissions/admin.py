from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'verdict', 'language', 'submitted_at')
    list_filter = ('verdict', 'language', 'submitted_at')
    search_fields = ('user__username', 'problem__name', 'problem__contest_id')
    ordering = ('-submitted_at',)
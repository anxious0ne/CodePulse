from django.contrib import admin
from .models import Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('contest_id', 'problem_index', 'name', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'contest_id', 'problem_index')
    ordering = ('contest_id', 'problem_index')

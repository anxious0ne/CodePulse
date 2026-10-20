from django.contrib import admin
from .models import InterviewQuestion, UserQuestionProgress


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty']
    search_fields = ['title', 'description']


@admin.register(UserQuestionProgress)
class UserQuestionProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_completed', 'is_bookmarked', 'completed_at']
    list_filter = ['is_completed', 'is_bookmarked']
    search_fields = ['user__username', 'question__title']

from rest_framework import serializers
from .models import InterviewQuestion, UserQuestionProgress


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['id', 'title', 'description', 'category', 'difficulty', 'link', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserQuestionProgressSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question.title', read_only=True)
    question_category = serializers.CharField(source='question.category', read_only=True)
    question_difficulty = serializers.CharField(source='question.difficulty', read_only=True)

    class Meta:
        model = UserQuestionProgress
        fields = [
            'id', 'question', 'question_title', 'question_category', 'question_difficulty',
            'is_completed', 'is_bookmarked', 'notes', 'completed_at'
        ]
        read_only_fields = ['id', 'question', 'question_title', 'question_category', 'question_difficulty']

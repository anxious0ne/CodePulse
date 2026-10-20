from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'goal_type',
            'target_value', 'current_value', 'deadline',
            'is_completed', 'progress_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'progress_percentage', 'created_at', 'updated_at']

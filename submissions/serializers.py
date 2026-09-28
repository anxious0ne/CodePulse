from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    problem_name = serializers.CharField(source='problem.name', read_only=True)
    problem_index = serializers.CharField(source='problem.problem_index', read_only=True)
    contest_id = serializers.IntegerField(source='problem.contest_id', read_only=True)
    problem_rating = serializers.IntegerField(source='problem.rating', read_only=True)
    tags = serializers.JSONField(source='problem.tags', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'contest_id',
            'problem_index',
            'problem_name',
            'problem_rating',
            'tags',
            'verdict',
            'language',
            'submitted_at',
        ]

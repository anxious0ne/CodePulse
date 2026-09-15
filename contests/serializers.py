from rest_framework import serializers
from .models import Contest


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = [
            'contest_id',
            'contest_name',
            'rank',
            'old_rating',
            'new_rating',
            'rating_update_time',
        ]
from rest_framework import serializers
from .models import Contest


class ContestSerializer(serializers.ModelSerializer):
    delta = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = [
            'contest_id',
            'contest_name',
            'rank',
            'old_rating',
            'new_rating',
            'delta',
            'rating_update_time',
        ]

    def get_delta(self, obj):
        return obj.new_rating - obj.old_rating
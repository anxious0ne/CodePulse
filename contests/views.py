from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contest
from .serializers import ContestSerializer


class ContestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ordering = request.query_params.get('ordering', 'rating_update_time')
        limit = request.query_params.get('limit')

        contests = Contest.objects.filter(user=request.user)

        if ordering in ['rating_update_time', '-rating_update_time', 'new_rating', '-new_rating']:
            contests = contests.order_by(ordering)
        else:
            contests = contests.order_by('rating_update_time')

        if limit and limit.isdigit():
            contests = contests[:int(limit)]

        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)
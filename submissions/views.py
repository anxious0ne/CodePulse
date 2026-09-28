from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Submission
from .serializers import SubmissionSerializer


class RecentSubmissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = request.query_params.get('limit', 25)
        try:
            limit = min(int(limit), 100)
        except ValueError:
            limit = 25

        verdict_filter = request.query_params.get('verdict')

        qs = Submission.objects.filter(user=request.user).select_related('problem')
        if verdict_filter:
            qs = qs.filter(verdict=verdict_filter)

        submissions = qs.order_by('-submitted_at')[:limit]
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

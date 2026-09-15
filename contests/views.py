from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contest
from .serializers import ContestSerializer

class ContestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contests = Contest.objects.filter(user=request.user).order_by('rating_update_time')
        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)
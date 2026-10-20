from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Goal
from .serializers import GoalSerializer


class GoalListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/goals/ — list authenticated user's goals
    POST /api/goals/ — create a new goal
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/goals/<id>/ — retrieve a goal
    PUT    /api/goals/<id>/ — update a goal
    PATCH  /api/goals/<id>/ — partial update
    DELETE /api/goals/<id>/ — delete a goal
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

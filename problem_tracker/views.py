from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Problem
from .serializers import ProblemSerializer


class ProblemListView(generics.ListAPIView):
    """
    GET /api/problems/
    Returns all problems. Supports optional filtering by rating and tag.
    """
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Problem.objects.all().order_by('contest_id', 'problem_index')
        rating = self.request.query_params.get('rating')
        tag = self.request.query_params.get('tag')

        if rating:
            try:
                queryset = queryset.filter(rating=int(rating))
            except ValueError:
                pass

        if tag:
            # JSONField contains list of strings, use __contains
            queryset = queryset.filter(tags__contains=tag)

        return queryset


class ProblemDetailView(generics.RetrieveAPIView):
    """
    GET /api/problems/<id>/
    Returns a single problem by primary key.
    """
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]
    queryset = Problem.objects.all()

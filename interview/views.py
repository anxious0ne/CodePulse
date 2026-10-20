from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import InterviewQuestion, UserQuestionProgress
from .serializers import InterviewQuestionSerializer, UserQuestionProgressSerializer


class InterviewQuestionListView(generics.ListAPIView):
    """
    GET /api/interview/questions/
    List all interview questions. Supports ?category= and ?difficulty= filters.
    """
    serializer_class = InterviewQuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = InterviewQuestion.objects.all()
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset


class UserProgressView(APIView):
    """
    GET  /api/interview/progress/<question_id>/ — get progress on a question
    PUT  /api/interview/progress/<question_id>/ — update progress
    """
    permission_classes = [IsAuthenticated]

    def _get_progress(self, user, question_id):
        try:
            question = InterviewQuestion.objects.get(id=question_id)
        except InterviewQuestion.DoesNotExist:
            return None, None
        progress, _ = UserQuestionProgress.objects.get_or_create(user=user, question=question)
        return question, progress

    def get(self, request, question_id):
        question, progress = self._get_progress(request.user, question_id)
        if question is None:
            return Response({'detail': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserQuestionProgressSerializer(progress)
        return Response(serializer.data)

    def put(self, request, question_id):
        question, progress = self._get_progress(request.user, question_id)
        if question is None:
            return Response({'detail': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserQuestionProgressSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            # Auto-set completed_at if marking as completed
            if request.data.get('is_completed') and not progress.completed_at:
                from django.utils import timezone
                serializer.save(completed_at=timezone.now())
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

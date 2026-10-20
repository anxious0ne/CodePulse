from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.InterviewQuestionListView.as_view(), name='interview-questions'),
    path('progress/<int:question_id>/', views.UserProgressView.as_view(), name='interview-progress'),
]

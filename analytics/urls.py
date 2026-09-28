from django.urls import path
from .views import (
    TopicAnalyticsView,
    VerdictAnalyticsView,
    RatingDistributionView,
)

urlpatterns = [
    path('topics/', TopicAnalyticsView.as_view(), name='analytics-topics'),
    path('verdicts/', VerdictAnalyticsView.as_view(), name='analytics-verdicts'),
    path('ratings/', RatingDistributionView.as_view(), name='analytics-ratings'),
]

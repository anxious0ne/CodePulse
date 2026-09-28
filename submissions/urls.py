from django.urls import path
from .views import RecentSubmissionsView

urlpatterns = [
    path('recent/', RecentSubmissionsView.as_view(), name='submissions-recent'),
]

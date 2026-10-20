from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users.views import (
    home_page,
    dashboard_page,
    DashboardSummaryView,
    SyncCodeforcesView,
    UpdateHandleView,
)
from contests.views import ContestListView
from analytics.views import (
    TopicAnalyticsView,
    VerdictAnalyticsView,
    RatingDistributionView,
)
from submissions.views import RecentSubmissionsView
from accounts.views import login_view, register_view, logout_view


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Web Pages
    path('', home_page, name='home'),
    path('home/', home_page, name='home-page'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('login/', login_view, name='login-direct'),
    path('register/', register_view, name='register-direct'),
    path('logout/', logout_view, name='logout-direct'),

    # Modular App URLs
    path('accounts/', include('accounts.urls')),
    path('users/', include('users.urls')),
    path('contests/', include('contests.urls')),
    path('analytics/', include('analytics.urls')),
    path('submissions/', include('submissions.urls')),

    # Direct REST API endpoints
    path('api/dashboard/', DashboardSummaryView.as_view(), name='api-dashboard'),
    path('api/contests/', ContestListView.as_view(), name='api-contests'),
    path('api/analytics/topics/', TopicAnalyticsView.as_view(), name='api-analytics-topics'),
    path('api/analytics/verdicts/', VerdictAnalyticsView.as_view(), name='api-analytics-verdicts'),
    path('api/analytics/ratings/', RatingDistributionView.as_view(), name='api-analytics-ratings'),
    path('api/submissions/recent/', RecentSubmissionsView.as_view(), name='api-submissions-recent'),
    path('api/codeforces/sync/', SyncCodeforcesView.as_view(), name='api-codeforces-sync'),
    path('api/codeforces/handle/', UpdateHandleView.as_view(), name='api-codeforces-handle'),
    path('api/profiles/handle/', UpdateHandleView.as_view(), name='api-profiles-handle'),

    # New app routes
    path('api/profile/', include('profiles.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/interview/', include('interview.urls')),
    path('api/codeforces/', include('codeforces.urls')),
    path('api/problems/', include('problem_tracker.urls')),
]

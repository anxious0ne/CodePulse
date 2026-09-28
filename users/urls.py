from django.urls import path
from .views import (
    dashboard_page,
    DashboardSummaryView,
    SyncCodeforcesView,
    UpdateHandleView,
)

urlpatterns = [
    path('', dashboard_page, name='dashboard'),
    path('api/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('api/sync/', SyncCodeforcesView.as_view(), name='dashboard-sync'),
    path('api/handle/', UpdateHandleView.as_view(), name='dashboard-handle'),
]
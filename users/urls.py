from django.urls import path
from .views import dashboard_page, DashboardSummaryView

urlpatterns = [
    path('', dashboard_page, name='dashboard'),
    path('api/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]
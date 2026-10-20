from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.CodeforcesConnectView.as_view(), name='cf-connect'),
    path('sync/', views.CodeforcesSyncView.as_view(), name='cf-sync'),
    path('status/', views.CodeforcesStatusView.as_view(), name='cf-status'),
]

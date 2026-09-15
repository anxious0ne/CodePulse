from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from contests.models import Contest
from submissions.models import Submission
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_page(request):
    return render(request, 'dashboard.html')

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_contests = Contest.objects.filter(user=user)
        latest_contest = user_contests.order_by('-rating_update_time').first()
        best_contest = user_contests.order_by('-new_rating').first()

        data = {
            'codeforces_handle': user.codeforces_handle,
            'current_rating': latest_contest.new_rating if latest_contest else None,
            'max_rating': best_contest.new_rating if best_contest else None,
            'total_submissions': Submission.objects.filter(user=user).count(),
            'problems_solved': Submission.objects.filter(user=user, verdict='OK')
                                                  .values('problem').distinct().count(),
        }
        return Response(data)
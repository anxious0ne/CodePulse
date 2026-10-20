from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from contests.models import Contest
from submissions.models import Submission
from .services import get_cf_rank_info, sync_user_codeforces


def home_page(request):
    """Public front/landing page introducing CodeTrack AI with Login/Signup CTAs."""
    return render(request, 'home.html', {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
    })


@login_required
def dashboard_page(request):
    # Detect if user is new vs returning
    is_new = request.session.pop('is_new_user', False)
    
    # If not explicitly in session, check if user joined very recently and has no submissions
    if not is_new and hasattr(request.user, 'date_joined') and request.user.date_joined:
        time_since_join = datetime.now(timezone.utc) - request.user.date_joined
        if time_since_join < timedelta(hours=2) and Submission.objects.filter(user=request.user).count() == 0:
            is_new = True

    return render(request, 'dashboard.html', {
        'user': request.user,
        'codeforces_handle': request.user.codeforces_handle or '',
        'is_new_user': is_new,
    })


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_contests = Contest.objects.filter(user=user)
        latest_contest = user_contests.order_by('-rating_update_time').first()
        best_contest = user_contests.order_by('-new_rating').first()

        current_rating = latest_contest.new_rating if latest_contest else None
        max_rating = best_contest.new_rating if best_contest else None
        rank_info = get_cf_rank_info(current_rating)
        max_rank_info = get_cf_rank_info(max_rating)

        # Rating delta from previous contest
        recent_two_contests = list(user_contests.order_by('-rating_update_time')[:2])
        if len(recent_two_contests) >= 2:
            rating_delta = recent_two_contests[0].new_rating - recent_two_contests[1].new_rating
        elif len(recent_two_contests) == 1:
            rating_delta = recent_two_contests[0].new_rating - recent_two_contests[0].old_rating
        else:
            rating_delta = 0

        total_submissions = Submission.objects.filter(user=user).count()
        problems_solved = Submission.objects.filter(user=user, verdict='OK').values('problem').distinct().count()
        solve_rate = round((problems_solved / total_submissions * 100), 1) if total_submissions > 0 else 0

        data = {
            'username': user.username,
            'codeforces_handle': user.codeforces_handle or '',
            'is_handle_verified': user.is_handle_verified,
            'current_rating': current_rating,
            'max_rating': max_rating,
            'rating_delta': rating_delta,
            'rank_title': rank_info['title'],
            'rank_color': rank_info['color'],
            'max_rank_title': max_rank_info['title'],
            'max_rank_color': max_rank_info['color'],
            'total_submissions': total_submissions,
            'problems_solved': problems_solved,
            'solve_rate': solve_rate,
            'contests_count': user_contests.count(),
            'last_contest_date': latest_contest.rating_update_time if latest_contest else None,
        }
        return Response(data)


class SyncCodeforcesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        handle = request.data.get('handle') or user.codeforces_handle

        if not handle:
            return Response(
                {"error": "Please provide a valid Codeforces handle."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = sync_user_codeforces(user, handle)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to sync Codeforces data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateHandleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        handle = request.data.get('handle', '').strip()

        if not handle:
            return Response(
                {"error": "Handle cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.contrib.auth import get_user_model
        from django.db import IntegrityError
        User = get_user_model()

        # Check if handle already taken by another account
        existing = User.objects.filter(codeforces_handle__iexact=handle).exclude(pk=user.pk).first()
        if existing:
            return Response(
                {"error": f"The handle '{handle}' is already linked to account '{existing.username}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user.codeforces_handle = handle
            user.is_handle_verified = False
            user.save(update_fields=['codeforces_handle', 'is_handle_verified'])
        except IntegrityError:
            return Response(
                {"error": f"The handle '{handle}' is already associated with another account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Optionally auto-sync if requested
        auto_sync = request.data.get('sync', False)
        if auto_sync:
            try:
                result = sync_user_codeforces(user, handle)
                return Response({
                    "message": f"Handle updated to {handle} and data synced successfully!",
                    "sync": result,
                })
            except Exception as e:
                return Response({
                    "message": f"Handle updated to {handle}, but sync failed: {str(e)}",
                    "error": str(e),
                }, status=status.HTTP_207_MULTI_STATUS)

        return Response({"message": f"Codeforces handle updated to {handle}."})

    def put(self, request):
        return self.post(request)
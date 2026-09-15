from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from submissions.models import Submission

class TopicAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = Submission.objects.filter(user=request.user).select_related('problem')

        tag_stats = {}
        for sub in submissions:
            for tag in sub.problem.tags:
                stats = tag_stats.setdefault(tag, {'attempted_problems': set(), 'solved_problems': set()})
                stats['attempted_problems'].add(sub.problem_id)
                if sub.verdict == 'OK':
                    stats['solved_problems'].add(sub.problem_id)

        result = [
            {
                'tag': tag,
                'attempted': len(stats['attempted_problems']),
                'solved': len(stats['solved_problems']),
                'solve_rate': round(len(stats['solved_problems']) / len(stats['attempted_problems']), 2),
            }
            for tag, stats in tag_stats.items()
        ]
        result.sort(key=lambda x: x['solve_rate'])  # weakest topics first
        return Response(result)
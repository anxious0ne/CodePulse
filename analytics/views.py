from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from submissions.models import Submission
from problem_tracker.models import Problem


class TopicAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = (
            Submission.objects.filter(user=request.user)
            .select_related('problem')
        )

        tag_stats = {}
        for sub in submissions:
            tags = sub.problem.tags or []
            for tag in tags:
                stats = tag_stats.setdefault(tag, {'attempted_problems': set(), 'solved_problems': set()})
                stats['attempted_problems'].add(sub.problem_id)
                if sub.verdict == 'OK':
                    stats['solved_problems'].add(sub.problem_id)

        result = []
        for tag, stats in tag_stats.items():
            attempted_cnt = len(stats['attempted_problems'])
            solved_cnt = len(stats['solved_problems'])
            rate = round(solved_cnt / attempted_cnt, 2) if attempted_cnt > 0 else 0
            result.append({
                'tag': tag,
                'attempted': attempted_cnt,
                'solved': solved_cnt,
                'solve_rate': rate,
            })

        # Weakest topics first, with secondary sort by attempted count descending
        result.sort(key=lambda x: (x['solve_rate'], -x['attempted']))
        return Response(result)


class VerdictAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = Submission.objects.filter(user=request.user)
        total = submissions.count()

        verdict_map = {
            'OK': 'Accepted',
            'WRONG_ANSWER': 'Wrong Answer',
            'TIME_LIMIT_EXCEEDED': 'Time Limit Exceeded',
            'RUNTIME_ERROR': 'Runtime Error',
            'COMPILATION_ERROR': 'Compilation Error',
            'OTHER': 'Other / Skipped',
        }

        counts = {k: 0 for k in verdict_map}
        for sub in submissions.values('verdict'):
            v = sub['verdict']
            if v in counts:
                counts[v] += 1
            else:
                counts['OTHER'] += 1

        data = [
            {
                'key': k,
                'label': verdict_map[k],
                'count': counts[k],
                'percentage': round((counts[k] / total * 100), 1) if total > 0 else 0,
            }
            for k in verdict_map
            if counts[k] > 0
        ]

        return Response({
            'total': total,
            'breakdown': data,
        })


class RatingDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solved_problem_ids = (
            Submission.objects.filter(user=request.user, verdict='OK')
            .values_list('problem_id', flat=True)
            .distinct()
        )

        solved_problems = Problem.objects.filter(
            id__in=solved_problem_ids,
            rating__isnull=False,
        ).values_list('rating', flat=True)

        brackets = [
            ('< 1000', 0, 999),
            ('1000-1199', 1000, 1199),
            ('1200-1399', 1200, 1399),
            ('1400-1599', 1400, 1599),
            ('1600-1899', 1600, 1899),
            ('1900-2199', 1900, 2199),
            ('2200-2399', 2200, 2399),
            ('2400-2599', 2400, 2599),
            ('2600+', 2600, 9999),
        ]

        counts = {b[0]: 0 for b in brackets}
        for rating in solved_problems:
            for label, low, high in brackets:
                if low <= rating <= high:
                    counts[label] += 1
                    break

        return Response([
            {'range': label, 'count': counts[label]}
            for label, _, _ in brackets
        ])
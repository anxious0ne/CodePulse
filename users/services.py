import requests
from datetime import datetime, timezone
from django.db import transaction
from contests.models import Contest
from problem_tracker.models import Problem
from submissions.models import Submission


def timestamp_to_datetime(timestamp):
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def get_cf_rank_info(rating):
    if rating is None:
        return {'title': 'Unrated', 'color': '#94a3b8'}
    if rating < 1200:
        return {'title': 'Newbie', 'color': '#9ca3af'}
    if rating < 1400:
        return {'title': 'Pupil', 'color': '#22c55e'}
    if rating < 1600:
        return {'title': 'Specialist', 'color': '#06b6d4'}
    if rating < 1900:
        return {'title': 'Expert', 'color': '#3b82f6'}
    if rating < 2100:
        return {'title': 'Candidate Master', 'color': '#a855f7'}
    if rating < 2300:
        return {'title': 'Master', 'color': '#f59e0b'}
    if rating < 2400:
        return {'title': 'International Master', 'color': '#f97316'}
    if rating < 2600:
        return {'title': 'Grandmaster', 'color': '#ef4444'}
    if rating < 3000:
        return {'title': 'International Grandmaster', 'color': '#dc2626'}
    return {'title': 'Legendary Grandmaster', 'color': '#b91c1c'}


def sync_user_codeforces(user, handle=None):
    """
    Synchronizes Codeforces user data:
    1. User profile details (rating, rank, maxRating, etc.)
    2. Contests rating history
    3. User submissions and associated problems
    """
    if handle:
        handle = handle.strip()
        user.codeforces_handle = handle

    if not user.codeforces_handle:
        raise ValueError("User does not have a Codeforces handle configured.")

    handle = user.codeforces_handle

    # 1. Fetch user info
    user_info = {}
    try:
        info_resp = requests.get(
            "https://codeforces.com/api/user.info",
            params={"handles": handle},
            timeout=15,
        )
        if info_resp.status_code == 200:
            data = info_resp.json()
            if data.get("status") == "OK" and data.get("result"):
                user_info = data["result"][0]
                user.is_handle_verified = True
                user.save(update_fields=["codeforces_handle", "is_handle_verified"])
    except requests.RequestException:
        # Proceed even if user.info times out, rating and status may still work
        pass

    # 2. Fetch rating history (contests)
    try:
        rating_resp = requests.get(
            "https://codeforces.com/api/user.rating",
            params={"handle": handle},
            timeout=20,
        )
        rating_resp.raise_for_status()
        contest_data = rating_resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Could not connect to Codeforces rating API: {e}")

    if contest_data.get("status") != "OK":
        raise ValueError(f"Codeforces API error: {contest_data.get('comment', 'Unknown error')}")

    # 3. Fetch submissions
    try:
        status_resp = requests.get(
            "https://codeforces.com/api/user.status",
            params={"handle": handle},
            timeout=30,
        )
        status_resp.raise_for_status()
        submission_data = status_resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Could not connect to Codeforces submissions API: {e}")

    if submission_data.get("status") != "OK":
        raise ValueError(f"Codeforces API error: {submission_data.get('comment', 'Unknown error')}")

    # Process contests
    contests_created = 0
    contests_updated = 0

    with transaction.atomic():
        for item in contest_data.get("result", []):
            _, created = Contest.objects.update_or_create(
                user=user,
                contest_id=item["contestId"],
                defaults={
                    "contest_name": item["contestName"],
                    "rank": item["rank"],
                    "old_rating": item["oldRating"],
                    "new_rating": item["newRating"],
                    "rating_update_time": timestamp_to_datetime(item["ratingUpdateTimeSeconds"]),
                },
            )
            if created:
                contests_created += 1
            else:
                contests_updated += 1

    # Process problems and submissions
    problems_created = 0
    problems_updated = 0
    submissions_created = 0

    allowed_verdicts = {
        "OK",
        "WRONG_ANSWER",
        "TIME_LIMIT_EXCEEDED",
        "RUNTIME_ERROR",
        "COMPILATION_ERROR",
        "CHALLENGED",
        "SKIPPED",
        "MEMORY_LIMIT_EXCEEDED",
    }

    with transaction.atomic():
        for item in submission_data.get("result", []):
            problem_data = item.get("problem", {})
            contest_id = problem_data.get("contestId")
            problem_index = problem_data.get("index")

            if contest_id is None or not problem_index:
                continue

            problem, p_created = Problem.objects.update_or_create(
                contest_id=contest_id,
                problem_index=problem_index,
                defaults={
                    "name": problem_data.get("name", ""),
                    "rating": problem_data.get("rating"),
                    "tags": problem_data.get("tags", []),
                },
            )
            if p_created:
                problems_created += 1
            else:
                problems_updated += 1

            verdict = item.get("verdict", "OTHER")
            if verdict not in allowed_verdicts:
                verdict = "OTHER"

            submitted_dt = timestamp_to_datetime(item.get("creationTimeSeconds"))
            if not submitted_dt:
                continue

            _, s_created = Submission.objects.get_or_create(
                user=user,
                problem=problem,
                submitted_at=submitted_dt,
                defaults={
                    "verdict": verdict,
                    "language": item.get("programmingLanguage", "Unknown"),
                },
            )
            if s_created:
                submissions_created += 1

    user.is_handle_verified = True
    user.save(update_fields=["codeforces_handle", "is_handle_verified"])

    return {
        "success": True,
        "handle": handle,
        "user_info": user_info,
        "contests_created": contests_created,
        "contests_updated": contests_updated,
        "problems_created": problems_created,
        "problems_updated": problems_updated,
        "submissions_created": submissions_created,
    }

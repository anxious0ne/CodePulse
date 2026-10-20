import requests
import hashlib
import random
import time
from datetime import datetime, timezone
from django.conf import settings
from django.db import transaction
from contests.models import Contest
from problem_tracker.models import Problem
from submissions.models import Submission


def call_codeforces_api(endpoint, params=None, timeout=20):
    """
    Calls a Codeforces API endpoint.
    If both CODEFORCES_API_KEY and CODEFORCES_API_SECRET are set,
    generates a SHA-512 signature per Codeforces authorization spec:
    https://codeforces.com/apiHelp
    Otherwise makes an anonymous request.
    """
    url = f"https://codeforces.com/api/{endpoint}"
    params = dict(params or {})

    api_key = getattr(settings, 'CODEFORCES_API_KEY', '').strip()
    api_secret = getattr(settings, 'CODEFORCES_API_SECRET', '').strip()

    if api_key and api_secret:
        rand = f"{random.randint(100000, 999999):06d}"
        cur_time = int(time.time())
        params['apiKey'] = api_key
        params['time'] = str(cur_time)

        sorted_param_pairs = sorted(params.items(), key=lambda kv: (kv[0], str(kv[1])))
        param_string = '&'.join(f"{k}={v}" for k, v in sorted_param_pairs)

        to_hash = f"{rand}/{endpoint}?{param_string}#{api_secret}"
        sha512_hash = hashlib.sha512(to_hash.encode('utf-8')).hexdigest()
        params['apiSig'] = f"{rand}{sha512_hash}"

    return requests.get(url, params=params, timeout=timeout)



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
        info_resp = call_codeforces_api("user.info", params={"handles": handle}, timeout=15)
        info_data = info_resp.json() if info_resp.content else {}
        if info_data.get("status") == "OK" and info_data.get("result"):
            user_info = info_data["result"][0]
            user.is_handle_verified = True
            user.save(update_fields=["codeforces_handle", "is_handle_verified"])
        elif info_data.get("status") == "FAILED":
            comment = info_data.get("comment", "")
            if "not found" in comment.lower():
                raise ValueError(
                    f"Codeforces user with handle '{handle}' was not found. "
                    "Please check your exact username at codeforces.com/profile/<handle>."
                )
            raise ValueError(f"Codeforces API error: {comment}")
    except requests.RequestException as e:
        # Proceed only on network/timeout errors
        pass

    # 2. Fetch rating history (contests)
    try:
        rating_resp = call_codeforces_api("user.rating", params={"handle": handle}, timeout=20)
        contest_data = rating_resp.json() if rating_resp.content else {}
        if contest_data.get("status") != "OK":
            comment = contest_data.get("comment", f"HTTP {rating_resp.status_code}")
            if "not found" in comment.lower():
                raise ValueError(
                    f"Codeforces user with handle '{handle}' was not found. "
                    "Please check your exact username at codeforces.com/profile/<handle>."
                )
            raise ValueError(f"Codeforces rating error: {comment}")
    except requests.RequestException as e:
        raise RuntimeError(f"Could not connect to Codeforces rating API: {e}")

    # 3. Fetch submissions
    try:
        status_resp = call_codeforces_api("user.status", params={"handle": handle}, timeout=30)
        submission_data = status_resp.json() if status_resp.content else {}
        if submission_data.get("status") != "OK":
            comment = submission_data.get("comment", f"HTTP {status_resp.status_code}")
            if "not found" in comment.lower():
                raise ValueError(
                    f"Codeforces user with handle '{handle}' was not found. "
                    "Please check your exact username at codeforces.com/profile/<handle>."
                )
            raise ValueError(f"Codeforces submissions error: {comment}")
    except requests.RequestException as e:
        raise RuntimeError(f"Could not connect to Codeforces submissions API: {e}")


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

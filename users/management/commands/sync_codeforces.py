import requests

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from contests.models import Contest
from problem_tracker.models import Problem
from submissions.models import Submission


class Command(BaseCommand):
    help = "Sync Codeforces contests, problems, and submissions for a user"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, **options):
        username = options["username"]

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' does not exist.")

        if not user.codeforces_handle:
            raise CommandError(
                f"User '{username}' does not have a Codeforces handle."
            )

        handle = user.codeforces_handle

        self.stdout.write(
            self.style.WARNING(
                f"Fetching Codeforces data for {handle}..."
            )
        )

        try:
            response = requests.get(
                "https://codeforces.com/api/user.rating",
                params={"handle": handle},
                timeout=15,
            )
            response.raise_for_status()
            contest_data = response.json()

            response = requests.get(
                "https://codeforces.com/api/user.status",
                params={"handle": handle},
                timeout=15,
            )
            response.raise_for_status()
            submission_data = response.json()

        except requests.RequestException as e:
            raise CommandError(f"Could not connect to Codeforces: {e}")

        if contest_data.get("status") != "OK":
            raise CommandError(
                f"Codeforces contest API error: {contest_data.get('comment', 'Unknown error')}"
            )

        if submission_data.get("status") != "OK":
            raise CommandError(
                f"Codeforces submission API error: {submission_data.get('comment', 'Unknown error')}"
            )

        contests_created = 0
        contests_updated = 0

        for item in contest_data["result"]:
            contest, created = Contest.objects.update_or_create(
                user=user,
                contest_id=item["contestId"],
                defaults={
                    "contest_name": item["contestName"],
                    "rank": item["rank"],
                    "old_rating": item["oldRating"],
                    "new_rating": item["newRating"],
                    "rating_update_time": self.timestamp_to_datetime(
                        item["ratingUpdateTimeSeconds"]
                    ),
                },
            )

            if created:
                contests_created += 1
            else:
                contests_updated += 1

        problems_created = 0
        problems_updated = 0
        submissions_created = 0

        for item in submission_data["result"]:
            problem_data = item.get("problem", {})

            contest_id = problem_data.get("contestId")
            problem_index = problem_data.get("index")

            # Some Codeforces submissions do not have a contestId.
            if contest_id is None or problem_index is None:
                continue

            problem, created = Problem.objects.update_or_create(
                contest_id=contest_id,
                problem_index=problem_index,
                defaults={
                    "name": problem_data.get("name", ""),
                    "rating": problem_data.get("rating"),
                    "tags": problem_data.get("tags", []),
                },
            )

            if created:
                problems_created += 1
            else:
                problems_updated += 1

            verdict = item.get("verdict", "OTHER")

            allowed_verdicts = {
                "OK",
                "WRONG_ANSWER",
                "TIME_LIMIT_EXCEEDED",
                "RUNTIME_ERROR",
                "COMPILATION_ERROR",
            }

            if verdict not in allowed_verdicts:
                verdict = "OTHER"

            Submission.objects.get_or_create(
                user=user,
                problem=problem,
                submitted_at=self.timestamp_to_datetime(
                    item["creationTimeSeconds"]
                ),
                defaults={
                    "verdict": verdict,
                    "language": item.get("programmingLanguage", "Unknown"),
                },
            )

            submissions_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Codeforces synchronization completed successfully."
            )
        )

        self.stdout.write(
            f"Contests: {contests_created} created, "
            f"{contests_updated} updated"
        )

        self.stdout.write(
            f"Problems: {problems_created} created, "
            f"{problems_updated} updated"
        )

        self.stdout.write(
            f"Submissions processed: {submissions_created}"
        )

    @staticmethod
    def timestamp_to_datetime(timestamp):
        from datetime import datetime, timezone

        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
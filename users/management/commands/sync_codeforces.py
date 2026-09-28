from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from users.services import sync_user_codeforces


class Command(BaseCommand):
    help = "Sync Codeforces contests, problems, and submissions for a user"

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--handle", dest="handle", default=None, help="Optional Codeforces handle override")

    def handle(self, *args, **options):
        username = options["username"]
        handle = options.get("handle")
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' does not exist.")

        if not handle and not user.codeforces_handle:
            raise CommandError(
                f"User '{username}' does not have a Codeforces handle configured."
            )

        active_handle = handle or user.codeforces_handle
        self.stdout.write(
            self.style.WARNING(f"Fetching Codeforces data for {active_handle}...")
        )

        try:
            res = sync_user_codeforces(user, handle=active_handle)
            self.stdout.write(
                self.style.SUCCESS("Codeforces synchronization completed successfully.")
            )
            self.stdout.write(
                f"Contests: {res['contests_created']} created, {res['contests_updated']} updated"
            )
            self.stdout.write(
                f"Problems: {res['problems_created']} created, {res['problems_updated']} updated"
            )
            self.stdout.write(
                f"Submissions processed: {res['submissions_created']}"
            )
        except Exception as e:
            raise CommandError(f"Sync failed: {e}")
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# username -> (env var suffix, is_superuser)
ACCOUNTS = {
    "waleed": ("WALEED", True),
    "adnan": ("ADNAN", False),
    "hamid": ("HAMID", False),
    "zain": ("ZAIN", False),
}


class Command(BaseCommand):
    help = "Create the fixed accounts (waleed, adnan, hamid, zain) from environment variables if they don't already exist."

    def handle(self, *args, **options):
        User = get_user_model()

        for username, (env_suffix, is_super) in ACCOUNTS.items():
            password = os.environ.get(f"DJANGO_{env_suffix}_PASSWORD")

            if not password:
                self.stdout.write(f"DJANGO_{env_suffix}_PASSWORD not set, skipping {username}.")
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"User '{username}' already exists, skipping.")
                continue

            if is_super:
                User.objects.create_superuser(username=username, email="", password=password)
            else:
                User.objects.create_user(username=username, email="", password=password)

            self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))

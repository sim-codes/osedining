#!/usr/bin/env python
"""
Create or update the Django admin (superuser) account non-interactively —
for hosts where you can only run a one-off script (like deploy.py), not an
interactive shell that `manage.py createsuperuser` normally prompts through.

Reads credentials from environment variables (or your .env file, same as
the rest of the app) rather than accepting them as arguments, so the
password never ends up in shell history or process listings:

    ADMIN_USERNAME   (defaults to "admin")
    ADMIN_EMAIL      (required)
    ADMIN_PASSWORD   (required)

Usage, from the project root with the app's virtualenv active:

    python create_admin.py

Safe to re-run: if the username already exists, it updates that account's
email/password and makes sure it's still staff+superuser, instead of
failing like `createsuperuser` does on a duplicate.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402


def main():
    username = os.environ.get("ADMIN_USERNAME", "admin")
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")

    if not email or not password:
        sys.exit(
            "ADMIN_EMAIL and ADMIN_PASSWORD must be set (as environment "
            "variables or in .env) before running this script."
        )

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username, defaults={"email": email}
    )
    user.email = email
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    print(f"{'Created' if created else 'Updated'} superuser '{username}' <{email}>.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Deployment script. Activate the app's virtualenv, then run this from the
project root:

    python deploy.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run(*args):
    print(f"$ {' '.join(args)}")
    subprocess.run(args, cwd=BASE_DIR, check=True)


def check_environment():
    if sys.prefix == sys.base_prefix:
        sys.exit(
            "No virtualenv is active for this interpreter "
            f"({sys.executable}). Activate the app's virtualenv first."
        )

    if not (BASE_DIR / "manage.py").exists():
        sys.exit(f"manage.py not found next to this script in {BASE_DIR} — wrong checkout?")

    print(f"Virtualenv: {sys.prefix}")
    print(f"Project dir: {BASE_DIR}")


def main():
    check_environment()
    run(sys.executable, "-m", "pip", "install", "-r", "requirements.txt")
    run(sys.executable, "manage.py", "migrate", "--noinput")
    run(sys.executable, "manage.py", "collectstatic", "--noinput")


if __name__ == "__main__":
    main()

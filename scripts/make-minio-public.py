# /// script
# dependencies = [
#   "python-dotenv",
# ]
# ///

import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

MEMBERS_FILE = Path(__file__).parent.parent / ".this-session-members.json"
DOTENV_FILE = Path(__file__).parent.parent / ".workshop-secrets.env"
MC_ALIAS = "workshop"
DEFAULT_MINIO_URL = "http://localhost:9000"


def run_mc(*args: str) -> None:
    """Run an mc command, raising on failure."""
    cmd = ["mc", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)

def main() -> None:
    load_dotenv(DOTENV_FILE)
    root_user = os.environ.get("MINIO_ROOT_USER")
    root_password = os.environ.get("MINIO_ROOT_PASSWORD")
    minio_url = os.environ.get("MINIO_URL", DEFAULT_MINIO_URL)

    if not root_user or not root_password:
        print("Error: MINIO_ROOT_USER and MINIO_ROOT_PASSWORD are required.")
        print(f"Set them in {DOTENV_FILE} or export them in your shell.")
        sys.exit(1)

    if not MEMBERS_FILE.exists():
        print(f"Error: {MEMBERS_FILE} not found.")
        print("Run 'uv run scripts/create-users.py' first to create workshop members.")
        sys.exit(1)

    members = json.loads(MEMBERS_FILE.read_text())

    print(f"Setting up mc alias '{MC_ALIAS}' -> {minio_url}")
    run_mc("alias", "set", MC_ALIAS, minio_url, root_user, root_password)

    bucket_count = 0

    for member in members:
        bucket_name = member.get("minio_username")
        if not bucket_name:
            email = member.get("email", "<unknown>")
            print(f"Error: member {email} is missing minio_username.")
            print("Run 'uv run scripts/create-minio-users.py' first.")
            sys.exit(1)

        print(f"  Ensuring bucket exists: {bucket_name}")
        run_mc("mb", "--ignore-existing", f"{MC_ALIAS}/{bucket_name}")

        print(f"  Making bucket public: {bucket_name}")
        run_mc("anonymous", "set", "download", f"{MC_ALIAS}/{bucket_name}")

        bucket_count += 1

    print(f"Done. Made {bucket_count} bucket(s) publicly downloadable.")


if __name__ == "__main__":
    main()
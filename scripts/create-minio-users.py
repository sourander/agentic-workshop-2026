# /// script
# dependencies = [
#   "python-dotenv",
# ]
# ///

import json
import os
import random
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

MEMBERS_FILE = Path(__file__).parent.parent / ".this-session-members.json"
DOTENV_FILE = Path(__file__).parent.parent / ".workshop-secrets.env"
MC_ALIAS = "workshop"
MINIO_URL = "http://127.0.0.1:9000"
GROUP_NAME = "workshop"


def run_mc(*args: str) -> None:
    """Run an mc command, raising on failure."""
    cmd = ["mc", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)


def generate_password(username: str) -> str:
    """Title-case the petname and append a random two-digit number."""
    titled = "-".join(part.capitalize() for part in username.split("-"))
    return f"{titled}{random.randint(10, 99)}"


def main() -> None:
    # Load env
    load_dotenv(dotenv_path=DOTENV_FILE)
    root_user = os.environ.get("MINIO_ROOT_USER")
    root_password = os.environ.get("MINIO_ROOT_PASSWORD")

    if not root_user or not root_password:
        print("Error: MINIO_ROOT_USER and MINIO_ROOT_PASSWORD are required.")
        print(f"Set them in {DOTENV_FILE} or export them in your shell.")
        sys.exit(1)

    # Read members
    if not MEMBERS_FILE.exists():
        print(f"Error: {MEMBERS_FILE} not found.")
        print("Run 'uv run scripts/create-users.py' first to create workshop members.")
        sys.exit(1)

    members = json.loads(MEMBERS_FILE.read_text())

    # Set up mc alias
    print(f"Setting up mc alias '{MC_ALIAS}' -> {MINIO_URL}")
    run_mc("alias", "set", MC_ALIAS, MINIO_URL, root_user, root_password)

    # Create users and add to group
    for member in members:
        email = member["email"]
        username = email.split("@")[0]
        password = generate_password(username)

        print(f"  Creating user: {username}")
        run_mc("admin", "user", "add", MC_ALIAS, username, password)
        run_mc("admin", "group", "add", MC_ALIAS, GROUP_NAME, username)

        member["minio_username"] = username
        member["minio_password"] = password

    # Attach policy to the group
    print(f"Attaching 'readwrite' policy to group '{GROUP_NAME}'")
    run_mc("admin", "policy", "attach", MC_ALIAS, "readwrite", f"--group={GROUP_NAME}")

    # Write updated members back
    MEMBERS_FILE.write_text(json.dumps(members, indent=2) + "\n")
    print(f"Updated {MEMBERS_FILE} with MinIO credentials.")
    print(f"Done. Created {len(members)} MinIO user(s).")


if __name__ == "__main__":
    main()

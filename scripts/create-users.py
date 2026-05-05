# /// script
# dependencies = [
#   "requests",
#   "python-dotenv",
#   "petname",
# ]
# ///

import json
import sys
from pathlib import Path

import petname
import requests
from dotenv import load_dotenv
import os

TARGET_MEMBER_COUNT = 50
EMAIL_DOMAIN = "foobar.local"
OUTPUT_FILE = Path(__file__).parent.parent / ".this-session-members.json"
DOTENV_FILE = Path(__file__).parent.parent / ".workshop-secrets.env"


def get_headers(api_key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key,
    }


def generate_unique_emails(count: int) -> list[str]:
    emails: list[str] = []
    seen: set[str] = set()
    while len(emails) < count:
        name = petname.generate(words=2, separator="-")
        email = f"{name}@{EMAIL_DOMAIN}"
        if email not in seen:
            seen.add(email)
            emails.append(email)
    return emails


def create_users(base_url: str, api_key: str, emails: list[str]) -> list[dict]:
    payload = [{"email": email, "role": "global:member"} for email in emails]
    r = requests.post(
        f"{base_url}/api/v1/users",
        headers=get_headers(api_key),
        json=payload,
    )
    r.raise_for_status()
    return r.json()


def build_output(response_items: list[dict]) -> list[dict]:
    records: list[dict] = []
    for item in response_items:
        if item.get("error"):
            print(f"Warning: failed to create user: {item['error']}")
            continue
        user = item.get("user", {})
        records.append({
            "email": user["email"],
            "n8n_invitation_url": user.get("inviteAcceptUrl", ""),
        })
    return records


def write_output(records: list[dict], path: Path) -> None:
    path.write_text(json.dumps(records, indent=2))
    print(f"Written {len(records)} record(s) to {path}")


def main() -> None:
    if OUTPUT_FILE.exists():
        print(f"Error: {OUTPUT_FILE} already exists.")
        print("This script is intended to run only once per workshop session.")
        print("If the workshop is still running, keep that file in a safe place.")
        print("If you want to start fresh, delete it manually and re-run the script.")
        sys.exit(1)

    load_dotenv(dotenv_path=DOTENV_FILE)

    api_key = os.environ.get("N8N_API_KEY")
    base_url = os.environ.get("N8N_BASE_URL", "http://localhost:5678")

    if not api_key or api_key == 'fetch-from-n8n-ui-and-add-here':
        print("Error: N8N_API_KEY environment variable is required.")
        print(f"Set it in {DOTENV_FILE} or export it in your shell.")
        sys.exit(1)

    print(f"Generating {TARGET_MEMBER_COUNT} unique email(s)...")
    new_emails = generate_unique_emails(TARGET_MEMBER_COUNT)

    print(f"Creating {TARGET_MEMBER_COUNT} user(s)...")
    response_items = create_users(base_url, api_key, new_emails)

    records = build_output(response_items)
    write_output(records, OUTPUT_FILE)
    print(f"Done. Created {len(records)} user(s).")


if __name__ == "__main__":
    main()
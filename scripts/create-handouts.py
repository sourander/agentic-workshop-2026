# /// script
# dependencies = []
# ///

import json
from datetime import date
from pathlib import Path

MEMBERS_FILE = Path(__file__).parent.parent / ".this-session-members.json"
OUTPUT_ROOT = Path(__file__).parent.parent / "handouts"

N8N_URL = "https://n8n-aika-agent-workshop.2.rahtiapp.fi"
MATTERMOST_URL = "https://mattermost-aika-agent-workshop.2.rahtiapp.fi"
MINIO_CONSOLE_URL = "https://minio-console-aika-agent-workshop.2.rahtiapp.fi"


def render_handout(member: dict, mattermost_invite_url: str) -> str:
    username = member["minio_username"]
    return f"""\
# Workshop Handout — {username}

## Services

| Service | URL |
|---------|-----|
| n8n | [{N8N_URL}]({N8N_URL}) |
| Mattermost | [{MATTERMOST_URL}]({MATTERMOST_URL}) |
| MinIO Console | [{MINIO_CONSOLE_URL}]({MINIO_CONSOLE_URL}) |

## Join Mattermost

[{mattermost_invite_url}]({mattermost_invite_url})

## Your Credentials

### n8n

- **Email:** {member["email"]}
- **Invitation link:** [{member["n8n_invitation_url"]}]({member["n8n_invitation_url"]})

### MinIO

- **Username:** {member["minio_username"]}
- **Password:** {member["minio_password"]}
"""


def main() -> None:
    if not MEMBERS_FILE.exists():
        print(f"Error: {MEMBERS_FILE} not found.")
        print("Run 'uv run scripts/create-users.py' first to create workshop members.")
        return

    members = json.loads(MEMBERS_FILE.read_text())

    mattermost_invite_url = input("Paste the Mattermost invite URL: ").strip()

    today = date.today().isoformat()
    output_dir = OUTPUT_ROOT / today
    output_dir.mkdir(parents=True, exist_ok=True)

    for member in members:
        username = member["minio_username"]
        out_file = output_dir / f"{username}.md"
        out_file.write_text(render_handout(member, mattermost_invite_url))
        print(f"Written: {out_file}")

    print(f"\nDone. {len(members)} handout(s) written to {output_dir}/")


if __name__ == "__main__":
    main()

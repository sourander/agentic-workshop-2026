# /// script
# dependencies = []
# ///

import argparse
import json
from datetime import date
from pathlib import Path
from textwrap import dedent

MEMBERS_FILE = Path(__file__).parent.parent / ".this-session-members.json"
OUTPUT_ROOT = Path(__file__).parent.parent / "handouts"

N8N_URL = "https://n8n-aika-agent-workshop.2.rahtiapp.fi"
MATTERMOST_URL = "https://mattermost-aika-agent-workshop.2.rahtiapp.fi"
MINIO_CONSOLE_URL = "https://minio-console-aika-agent-workshop.2.rahtiapp.fi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate workshop handout Markdown files.",
    )
    parser.add_argument(
        "variant",
        nargs="?",
        choices=("full", "mini"),
        default="full",
        help="Generate the regular handout or the miniworkshop version.",
    )
    return parser.parse_args()


def render_handout(
    member: dict,
    mattermost_invite_url: str | None = None,
    *,
    mini: bool = False,
) -> str:
    username = member.get("minio_username") or member["email"].split("@")[0]
    service_rows = [f"| n8n | [{N8N_URL}]({N8N_URL}) |"]
    if not mini:
        service_rows.extend(
            [
                f"| Mattermost | [{MATTERMOST_URL}]({MATTERMOST_URL}) |",
                f"| MinIO Console | [{MINIO_CONSOLE_URL}]({MINIO_CONSOLE_URL}) |",
            ]
        )

    sections = [
        dedent(
            f"""
            # Workshop Handout — {username}

            ## Services

            | Service | Link |
            |---------|------|
            {chr(10).join(service_rows)}
            """
        ).strip()
    ]

    if not mini:
        sections.append(
            dedent(
                f"""
                ## Join Mattermost

                [Open Mattermost invite]({mattermost_invite_url})
                """
            ).strip()
        )

    credentials_section = dedent(
        f"""
        ## Your Credentials

        ### n8n

        - **Email:** {member["email"]}
        - **Invitation link:** [Open n8n invitation]({member["n8n_invitation_url"]})
        """
    ).strip()

    if not mini:
        credentials_section += "\n\n" + dedent(
            f"""
            ### MinIO

            - **Username:** {member["minio_username"]}
            - **Password:** {member["minio_password"]}
            """
        ).strip()

    sections.append(credentials_section)

    return "\n\n".join(sections) + "\n"


def main() -> None:
    args = parse_args()

    if not MEMBERS_FILE.exists():
        print(f"Error: {MEMBERS_FILE} not found.")
        print("Run 'uv run scripts/create-users.py' first to create workshop members.")
        return

    members = json.loads(MEMBERS_FILE.read_text())
    mini = args.variant == "mini"

    mattermost_invite_url = None
    if not mini:
        mattermost_invite_url = input("Paste the Mattermost invite URL: ").strip()

    today = date.today().isoformat()
    output_dir = OUTPUT_ROOT / today
    output_dir.mkdir(parents=True, exist_ok=True)

    for member in members:
        username = member.get("minio_username") or member["email"].split("@")[0]
        out_file = output_dir / f"{username}.md"
        out_file.write_text(
            render_handout(member, mattermost_invite_url, mini=mini)
        )
        print(f"Written: {out_file}")

    variant_label = "mini " if mini else ""
    print(f"\nDone. {len(members)} {variant_label}handout(s) written to {output_dir}/")


if __name__ == "__main__":
    main()

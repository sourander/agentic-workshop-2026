---
icon: lucide/log-in
---

# Before You Start

!!! info
    Participants should be able to use this guide in two ways: by following along with a live instructor demo or by completing the same steps independently at their own pace.

## What you will receive

- Public n8n URL: `https://n8n-aika-agent-workshop.2.rahtiapp.fi`
- Username and password for your participant account: [Placeholder]
- Mattermost workspace URL: `https://mattermost-aika-agent-workshop.2.rahtiapp.fi`
- Mattermost invite link or support channel instructions: [Placeholder]
- MinIO API URL: `https://minio-api-aika-agent-workshop.2.rahtiapp.fi`
- MinIO console URL: `https://minio-console-aika-agent-workshop.2.rahtiapp.fi`
- MinIO credentials if the exercise requires file uploads: [Placeholder]

The table below has defaults that are 99,9 % sure to be correct, but verify with the instructor. URLs might get changed for security or technical reasons.

| Service       | Default URL                                                                                                | Notes                                 |
| ------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| n8n           | [n8n-aika-agent-workshop.2.rahtiapp.fi](https://n8n-aika-agent-workshop.2.rahtiapp.fi)                     | The key site.                         |
| Mattermost    | [mattermost-aika-agent-workshop.2.rahtiapp.fi](https://mattermost-aika-agent-workshop.2.rahtiapp.fi)       | Chat platform.                        |
| MinIO API     | [minio-api-aika-agent-workshop.2.rahtiapp.fi](https://minio-api-aika-agent-workshop.2.rahtiapp.fi)         | For API calls.                        |
| MinIO Console | [minio-console-aika-agent-workshop.2.rahtiapp.fi](https://minio-console-aika-agent-workshop.2.rahtiapp.fi) | For manual file uploads and browsing. |

What the instructor will hand you are two things:

### 1: JSON for credentials

```json
{
    "email": "clever-mayfly@foobar.local",
    "n8n_invitation_url": "https://n8n-aika-agent-workshop.2.rahtiapp.fi/signup?token=really-long-token-here",
    "minio_username": "clever-mayfly",
    "minio_password": "Clever-Mayfly14"
}
```

### 2: Mattermost invite link

It will look like this, and is same for all participants:

```
https://mattermost-aika-agent-workshop.2.rahtiapp.fi/signup_user_complete/?id=short-token-here
```

!!! tip

    At this point, create a local storage where you can save anything you need during the workshop. Prefer a simple tool like Notepad or Notes app. You can choose e.g.:

    * A Notes app, or
    * A Notepad saving a typical TXT file on your desktop, or
    * Any other tool that allows writing down and saving text information.

    Use whatever notetaking tool you like, but please save credentials, URLs, passwords, tokens and similar information so that you do not lose it.

## How to use this guide

- Follow the numbered phases in order.
- Pause after each success check before moving on.
- If your screen does not match the instructions, compare against the screenshot placeholder for that phase.
- If you get stuck, import the matching workflow JSON placeholder and continue from the next phase.

## Workshop flow

Continue to the next page to start the hands-on exercise.

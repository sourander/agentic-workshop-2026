---
icon: lucide/rocket
---

# Deployment Guide

!!! warning

    This whole "Instructor" section is intended only for the instructor(s) who will be running the workshop. If you are a participant, please skip this section and refer to the **Participant** part of the documentation.

## Before the workshop

- Confirm you have an ==OpenAI API token== with sufficient quota for the workshop exercises. This will be shared with the participants through the internal proxy.
- Confirm you have access to a CSC project with Rahti enabled.
- Decide the project name you want to use, or keep the default `aika-agent-workshop`.
- Build and push the custom Mattermost image before workshop day.
- Claim the first admin accounts before making the services public.
- Prepare the participant guide with screenshots and workflow JSON exports.
- Keep the admin credentials, Mattermost invite link, and workshop URLs in a local git-ignored note (`.secret`).

## Prerequisites

Install the following tools before deploying:

- `oc` for OpenShift access
- `docker` for building and pushing images
- `just` for task execution
- `envsubst` for manifest templating
- `uv` for running the helper scripts
- `mc` for MinIO administration

## Optional configuration

The default OpenShift project name is `aika-agent-workshop`. Override it when needed:

``` bash
export PROJECT_NAME=my-custom-name
```

All `just` recipes derive image paths and hostnames from that value.

## Set up access to Rahti

1. Create or identify the CSC project that has Rahti enabled.
2. Open `https://rahti.csc.fi/`.
3. Use the web console action to copy the login command and run it locally.

    ``` bash
    oc login \
    --token=sha256 \
    --server=https://api.2.rahti.csc.fi:6443
    ```

4. Create the OpenShift project if needed, using the My CSC project number in the description.

    ``` bash
    oc new-project \
    aika-agent-workshop \
    --description='csc_project: 201xxxx'

    oc project
    ```

5. Log in to the image registry.

    ``` bash
    docker login -p $(oc whoami -t) -u unused image-registry.apps.2.rahti.csc.fi
    ```

## Build and push the Mattermost image

Mattermost's upstream image expects root. The custom Dockerfile under `n8n/rahti/` adjusts file permissions so it can run on OKD as a non-root user.

Build the image:

``` bash
just build
```

Push the image to the Rahti registry:

``` bash
just push
```

Verify the image stream exists:

``` bash
oc get imagestream
```

!!! warning "Apple Silicon"
    The Mattermost image uses `linux/amd64`. On Apple Silicon, ensure Docker Desktop has Rosetta emulation enabled for x86_64 or amd64 containers before building.

## Deploy the workshop infrastructure

The deployment should stay internal until the first admin accounts are claimed.

### 1. Create the workshop secrets

Export the OpenAI token first:

``` bash
export OPENAI_API_KEY=sk-...
```

Then create the workshop secrets:

``` bash
just create-secrets
```

This writes `.workshop-secrets.env`, which is git-ignored and should remain local. The matching secrets are added into the OpenShift project as Secrets.

!!! warning
    `just create-secrets` now refuses to continue if `OPENAI_API_KEY` is not exported in the local shell.

### 2. Deploy the services without public routes

``` bash
just deploy
just wait # this will take a minute or two
just status
```

At this point, the deployments, services, and volumes should be present, but no public routes should be open yet.

### 3. Claim the admin accounts

Do this before exposing any public routes so the first admin account is not claimed by someone else.

#### Claim the n8n admin account

``` bash
just port-forward-n8n
```

Then open `http://localhost:5678` and complete the setup wizard.

- create the instructor admin account
- save the username and password in a local git-ignored note

#### Claim the Mattermost admin account

``` bash
just port-forward-mm
```

Then open `http://localhost:8065` and create the admin account. Use the same email and password as the n8n admin to keep things simple.

!!! tip
    Copy the Mattermost invite link during the initial setup and save it with the rest of the workshop secrets. That avoids an extra recovery step later.

### 4. Expose the public routes

``` bash
just expose
just status
```

This prints the public URLs for:

- n8n
- Mattermost
- MinIO API
- MinIO Console

## Create participant accounts

Create an n8n API key from the n8n UI under Settings, then fill in `N8N_API_KEY` and `N8N_BASE_URL` in `.workshop-secrets.env`.

Run:

``` bash
just create-n8n-users
```

This creates `.this-session-members.json`, including the generated petname accounts and their invitation URLs.

Example account naming:

- `happy-dolphin`
- `cosmic-oriole`

## Recover or regenerate the Mattermost invite link

If you did not copy the invite link during the initial Mattermost setup:

1. Open Mattermost as the admin user.
2. Use the `+` action.
3. Select Invite People.
4. Copy the invite link.

It should look similar to:

``` text
https://mattermost-aika-agent-workshop.2.rahtiapp.fi/signup_user_complete/?id=abd1234567890
```

## Create MinIO users

Start the MinIO port forward in one terminal:

``` bash
just port-forward-minio
```

Then create the users in another terminal:

``` bash
just create-minio-users
```

This reads `.this-session-members.json`, adds MinIO credentials for each participant, and writes the updated data back to the same file.

The resulting schema looks like this:

``` json
[
  {
    "email": "cosmic-oriole@foobar.local",
    "n8n_invitation_url": "https://n8n-aika-agent-workshop.2.rahtiapp.fi/signup?token=<really-long-token>",
    "minio_username": "cosmic-oriole",
    "minio_password": "Cosmic-Oriole95"
  }
]
```

## Workshop-day operations

- Verify the public routes with `just status` before participants arrive.
- Keep the admin credentials and invite links available in a private note.
- Instruct participants to configure their n8n OpenAI credential with base URL `http://openai-proxy/v1` and any placeholder token value. The internal proxy replaces the Authorization header with the workshop token.
- Share the n8n access details and participant credentials at the start of the session.

??? info "Suggested instructor handoff bundle"
    Keep the following items together for the session:

    - n8n URL
    - Mattermost URL and invite link
    - participant account list from `.this-session-members.json`
    - MinIO credentials
    - workflow JSON exports used as rescue imports

## Cleanup after the workshop

Delete the deployed workshop resources:

``` bash
just teardown
```

This removes the deployments, services, routes, PVCs, secrets, and the generated `.this-session-members.json` file.

Verify cleanup:

``` bash
oc get all,pvc,secret
```

Delete the OpenShift project as a final step if you no longer need it:

``` bash
oc delete project aika-agent-workshop
```

!!! warning
    Teardown permanently deletes all persistent workshop data, including n8n workflows, Mattermost messages, MinIO data, and database contents.
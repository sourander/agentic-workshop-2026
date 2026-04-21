---
icon: lucide/graduation-cap
---

# Good to Know

!!! warning

    This whole "Instructor" section is intended only for the instructor(s) who will be running the workshop. If you are a participant, please skip this section and refer to the **Participant** part of the documentation.

## Workshop overview

The workshop stack consists of:

- n8n as the main automation environment used by participants
- Mattermost for communication and participant invites
- MinIO for object storage and workshop assets
- CSC Rahti as the recommended hosting environment for shared workshop delivery

Use CSC Rahti for the actual workshop unless you are doing a quick local dry run. Rahti is only slightly more work than local Docker Compose, and it matches the environment that participants will use.

## Delivery modes

### Recommended: CSC Rahti

Use Rahti when you need:

- public access for participants
- shared collaboration during the workshop
- the same URLs and account flow that participants will actually use

This is instructed in the [Deployment Guide](02_deployment.md).

### Optional: local Docker Compose

Use local Compose for a short dry run or content rehearsal.

``` bash
cd n8n/compose
docker compose up -d
```

The local services are then available at:

- `http://localhost:5678` for n8n
- `http://localhost:9001` for the MinIO console
- `http://localhost:8065` for Mattermost

!!! note
    Local Compose is mainly useful for testing. The workshop itself is better delivered from Rahti because it gives participants public access to the same shared environment.

## Repository layout

| Path           | Purpose                                               |
| -------------- | ----------------------------------------------------- |
| `docs/`        | Zensical documentation source                         |
| `n8n/compose/` | Local Docker Compose files for dry runs               |
| `n8n/rahti/`   | CSC Rahti deployment manifests and image build assets |
| `scripts/`     | Helper scripts for secrets, users, and MinIO accounts |
| `Justfile`     | Common operational commands for the workshop          |
# Agentic Workshop 2026

## How to get started

### Locally

Check the [n8n/compose/README.md](./n8n/compose/README.md) for instructions on how to run the workshop locally using Docker Compose.

### On CSC Rahti

Check the [n8n/rahti/README.md](./n8n/rahti/README.md) for instructions on how to deploy the workshop on CSC Rahti. The file `Justfile` in the root directory is used to run common commands.

## Directory Structure

Planned directory structure draft:

```
agentic-workshop-2026/
├── docs/                       # zensical project
├── n8n/                        # n8n-specific workshop material
│   ├── compose/                # docker compose files for local dev/testing
│   └── rahti/                  # CSC Rahti deployment material
│
├── examples/                   # code/examples shared across docs and n8n
│   ├── prompts/
│   ├── sample-inputs/
│   ├── sample-outputs/
│   └── simple-automations/
│
├── scripts/                    # helper scripts
│
├── .github/
│   └── workflows/              # GitHub Pages deployment workflow
│
├── notes/                      # private prep notes, checklists, runbooks
│   ├── facilitator/
│   └── troubleshooting/
│
└── archive/                    # optional post-workshop exports/material
```
# Workshop deployment on CSC Rahti (OKD)
# Usage: just <recipe>

# Configuration
project_name := env("PROJECT_NAME", "aika-agent-workshop")
rahti_registry := "image-registry.apps.2.rahti.csc.fi"

# List available recipes
default:
    @just --list

# Build the custom Mattermost image for OKD
build:
    docker build \
        -t mattermost-okd \
        -f n8n/rahti/mattermost.Dockerfile \
        n8n/rahti

# Tag and push the Mattermost image to CSC's image registry
push:
    docker tag mattermost-okd {{ rahti_registry }}/{{ project_name }}/mattermost:latest
    docker push {{ rahti_registry }}/{{ project_name }}/mattermost:latest

# Generate random passwords and create the workshop-secrets OpenShift secret
create-secrets:
    bash scripts/create-secrets.sh

# Delete the workshop-secrets OpenShift secret (allows re-creation)
delete-secrets:
    oc delete secret workshop-secrets

# Deploy services (without public routes) using envsubst for templating
# NOTE: Run 'just create-secrets' first if the secret does not exist yet.
deploy:
    PROJECT_NAME={{ project_name }} envsubst '$$PROJECT_NAME' < n8n/rahti/workshop.yaml | oc apply -f -


# Wait for all deployments to be ready
wait:
    oc rollout status deployment/mattermost-db --timeout=120s
    oc rollout status deployment/minio --timeout=120s
    oc rollout status deployment/n8n --timeout=120s
    oc rollout status deployment/mattermost --timeout=180s

# Port-forward n8n to localhost:5678 (claim admin account before exposing routes)
port-forward-n8n:
    @echo "Open http://localhost:5678 and complete the setup wizard"
    oc port-forward svc/n8n 5678:5678

# Port-forward Mattermost to localhost:8065 (claim admin account before exposing routes)
port-forward-mm:
    @echo "Open http://localhost:8065 and create the admin account"
    oc port-forward svc/mattermost 8065:8065

# Port-forward MinIO Console to localhost:9001 (verify admin login before exposing routes)
port-forward-minio:
    @echo "Use local mc tool to e.g. add users and buckets"
    oc port-forward svc/minio 9000:9000

# Creates the n8n users and writes them to .this-session-members.json (assumes 'just expose' being run)
create-n8n-users:
    uv run scripts/create-users.py

# Create MinIO users from .this-session-members.json (Run 'just port-forward-minio' in another terminal first!)
create-minio-users:
    uv run scripts/create-minio-users.py

# Expose public routes (run AFTER claiming admin accounts)
expose:
    PROJECT_NAME={{ project_name }} envsubst '$$PROJECT_NAME' < n8n/rahti/routes.yaml | oc apply -f -
    @echo ""
    @echo "Public URLs:"
    @echo "  n8n:            https://n8n-{{ project_name }}.2.rahtiapp.fi"
    @echo "  Mattermost:     https://mattermost-{{ project_name }}.2.rahtiapp.fi"
    @echo "  MinIO API:      https://minio-api-{{ project_name }}.2.rahtiapp.fi"
    @echo "  MinIO Console:  https://minio-console-{{ project_name }}.2.rahtiapp.fi"


# Show status of pods, services, and routes
status:
    oc get pods,svc,routes

# Delete all workshop resources (PVCs, secrets, deployments, services, routes)
teardown:
    @echo "This will delete ALL workshop resources including persistent data."
    @echo "Press Ctrl+C within 5 seconds to cancel..."
    @sleep 5
    -PROJECT_NAME={{ project_name }} envsubst '$$PROJECT_NAME' < n8n/rahti/routes.yaml | oc delete -f -
    -PROJECT_NAME={{ project_name }} envsubst '$$PROJECT_NAME' < n8n/rahti/workshop.yaml | oc delete -f -
    -oc delete secret workshop-secrets
    @echo "Deleting the .this-session-members.json file with generated user info..."
    rm -f .this-session-members.json
    @echo ""
    @echo "All workshop resources deleted."
    @echo "To also delete the OKD project itself, run:"
    @echo "  oc delete project {{ project_name }}"

#!/usr/bin/env bash
set -euo pipefail

# ── Configuration (fixed, non-sensitive values) ─────────────────────────────
MINIO_ROOT_USER="minioadmin"
POSTGRES_USER="mmuser"
POSTGRES_DB="mattermost"

SECRET_NAME="workshop-secrets"
LOCAL_FILE=".workshop-secrets.env"

OPENAI_API_KEY=${OPENAI_API_KEY:-}
PROJECT_NAME=${PROJECT_NAME:-aika-agent-workshop}

# ── Pre-flight checks ───────────────────────────────────────────────────────
if ! command -v oc &>/dev/null; then
    echo "ERROR: 'oc' CLI not found. Install it first." >&2
    exit 1
fi

if ! oc whoami &>/dev/null; then
    echo "ERROR: Not logged in to OpenShift. Run 'oc login' first." >&2
    exit 1
fi

if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "WARNING: OPENAI_API_KEY is not set. Export an OpenAI API token before running this script." >&2
    exit 1
fi

if oc get secret "$SECRET_NAME" &>/dev/null; then
    echo "ERROR: Secret '$SECRET_NAME' already exists in namespace '$(oc project -q)'." >&2
    echo "       To recreate, delete it first:  just delete-secrets" >&2
    exit 1
fi

# ── Generate random passwords ───────────────────────────────────────────────
MINIO_ROOT_PASSWORD=$(openssl rand -base64 18 | tr -d '/+=')
POSTGRES_PASSWORD=$(openssl rand -base64 18 | tr -d '/+=')

# Derived connection string
MM_SQLSETTINGS_DATASOURCE="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@mattermost-db:5432/${POSTGRES_DB}?sslmode=disable&connect_timeout=10"

# Local MinIO API URL for temporary port-forwarded access, plus public service URLs
MINIO_URL="http://127.0.0.1:9000"
N8N_BASE_URL="https://n8n-${PROJECT_NAME}.2.rahtiapp.fi"
N8N_API_KEY=fetch-from-n8n-ui-and-add-here

# ── Create the OpenShift secret ─────────────────────────────────────────────
oc create secret generic "$SECRET_NAME" \
    --from-literal="MINIO_ROOT_USER=${MINIO_ROOT_USER}" \
    --from-literal="MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}" \
    --from-literal="POSTGRES_USER=${POSTGRES_USER}" \
    --from-literal="POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" \
    --from-literal="POSTGRES_DB=${POSTGRES_DB}" \
    --from-literal="MM_SQLSETTINGS_DATASOURCE=${MM_SQLSETTINGS_DATASOURCE}" \
    --from-literal="OPENAI_API_KEY=${OPENAI_API_KEY}"

# ── Save credentials locally ────────────────────────────────────────────────
cat > "$LOCAL_FILE" <<EOF
# Workshop secrets — generated $(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Namespace: $(oc project -q)
MINIO_ROOT_USER='${MINIO_ROOT_USER}'
MINIO_ROOT_PASSWORD='${MINIO_ROOT_PASSWORD}'
MINIO_URL='${MINIO_URL}'
POSTGRES_USER='${POSTGRES_USER}'
POSTGRES_PASSWORD='${POSTGRES_PASSWORD}'
POSTGRES_DB='${POSTGRES_DB}'
MM_SQLSETTINGS_DATASOURCE='${MM_SQLSETTINGS_DATASOURCE}'
N8N_BASE_URL='${N8N_BASE_URL}'
N8N_API_KEY='${N8N_API_KEY}'
EOF

chmod 600 "$LOCAL_FILE"

echo ""
echo "Secret '$SECRET_NAME' created in namespace '$(oc project -q)'."
echo "Credentials saved to $LOCAL_FILE"
echo ""
echo "  MINIO_ROOT_USER      = ${MINIO_ROOT_USER}"
echo "  MINIO_ROOT_PASSWORD  = ${MINIO_ROOT_PASSWORD}"
echo "  MINIO_URL            = ${MINIO_URL}"
echo "  POSTGRES_USER        = ${POSTGRES_USER}"
echo "  POSTGRES_PASSWORD    = ${POSTGRES_PASSWORD}"
echo "  POSTGRES_DB          = ${POSTGRES_DB}"
echo ""
echo " Remember to fetch the n8n API key from the n8n UI and add it to the .workshop-secrets.env file."

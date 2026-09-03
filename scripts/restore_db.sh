#!/usr/bin/env bash
# ==============================================================================
# FavvMenuz Database Restore Script
# Restores a compressed PostgreSQL dump file into the running database container.
# Requires explicit confirmation to prevent accidental data overwrites.
# ==============================================================================

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path_to_backup_file.sql.gz> [--force]"
    exit 1
fi

BACKUP_FILE="$1"
FORCE_FLAG="${2:-}"
CONTAINER_NAME="${CONTAINER_NAME:-favvmenuz_db}"
DB_NAME="${POSTGRES_DB:-favvmenuz_db}"
DB_USER="${POSTGRES_USER:-favvmenuz_user}"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "[ERROR] Backup file not found: ${BACKUP_FILE}" >&2
    exit 1
fi

if [ "${FORCE_FLAG}" != "--force" ]; then
    echo "======================================================================"
    echo "WARNING: This will DESTROY and OVERWRITE all existing data in '${DB_NAME}'!"
    echo "Backup file to restore: ${BACKUP_FILE}"
    echo "Target container: ${CONTAINER_NAME}"
    echo "======================================================================"
    read -rp "Are you absolutely sure you want to proceed? (Type 'yes' to confirm): " CONFIRMATION
    if [ "${CONFIRMATION}" != "yes" ]; then
        echo "[ABORTED] Database restoration cancelled."
        exit 0
    fi
fi

echo "[INFO] Restoring database '${DB_NAME}' from ${BACKUP_FILE}..."

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    gunzip -c "${BACKUP_FILE}" | docker exec -i "${CONTAINER_NAME}" psql -U "${DB_USER}" -d "${DB_NAME}"
    echo "[SUCCESS] Database restoration completed successfully."
else
    echo "[ERROR] Target database container '${CONTAINER_NAME}' is not running." >&2
    exit 1
fi

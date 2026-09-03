#!/usr/bin/env bash
# ==============================================================================
# FavvMenuz Database Backup Script
# Creates a timestamped PostgreSQL dump inside the ./backups directory.
# ==============================================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
CONTAINER_NAME="${CONTAINER_NAME:-favvmenuz_db}"
DB_NAME="${POSTGRES_DB:-favvmenuz_db}"
DB_USER="${POSTGRES_USER:-favvmenuz_user}"

mkdir -p "${BACKUP_DIR}"

BACKUP_FILE="${BACKUP_DIR}/favvmenuz_backup_${TIMESTAMP}.sql.gz"

echo "[INFO] Starting database backup for database '${DB_NAME}'..."
echo "[INFO] Target file: ${BACKUP_FILE}"

# Check if Docker is running and container exists
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker exec -t "${CONTAINER_NAME}" pg_dump -U "${DB_USER}" -d "${DB_NAME}" --clean --if-exists | gzip > "${BACKUP_FILE}"
    echo "[SUCCESS] Backup created successfully at ${BACKUP_FILE}"
    echo "[NOTE] Keep backups safe. A backup on the same disk will not protect against host disk failures."
else
    echo "[ERROR] Database container '${CONTAINER_NAME}' is not running." >&2
    exit 1
fi

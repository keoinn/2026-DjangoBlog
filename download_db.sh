#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Downloading Database from Google Drive..."
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "${SCRIPT_DIR}/config.sh" ]; then
    source "${SCRIPT_DIR}/config.sh"
else
    echo "[ERROR] config.sh not found."
    exit 1
fi

echo "Target: ${DB_PATH}"

if command -v curl &> /dev/null; then
    echo "Using curl to download..."
    curl -L "${DOWNLOAD_URL}" -o "${DB_PATH}"
elif command -v wget &> /dev/null; then
    echo "Using wget to download..."
    wget -O "${DB_PATH}" "${DOWNLOAD_URL}"
else
    echo "[ERROR] Neither curl nor wget is installed."
    exit 1
fi

if [ ! -s "${DB_PATH}" ]; then
    echo "[ERROR] Database file was not created or is empty."
    exit 1
fi

echo "=========================================="
echo "Database downloaded successfully!"
echo "Saved as: ${DB_PATH}"
echo "=========================================="

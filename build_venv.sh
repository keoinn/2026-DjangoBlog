#!/bin/sh
set -e

echo "=========================================="
echo "Setting up Python Virtual Environment..."
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is not installed or not in PATH."
    exit 1
fi

# Create virtual environment
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv "${SCRIPT_DIR}/.venv"
    echo "Virtual environment created successfully."
else
    echo ".venv already exists. Skipping creation."
fi

# Upgrade pip using python3
echo "Upgrading pip..."
"${SCRIPT_DIR}/.venv/bin/python3" -m pip install --upgrade pip

# Install dependencies
if [ -f "${SCRIPT_DIR}/requirement.txt" ]; then
    echo "Installing dependencies from requirement.txt..."
    "${SCRIPT_DIR}/.venv/bin/python3" -m pip install -r "${SCRIPT_DIR}/requirement.txt"
else
    echo "[WARNING] requirement.txt not found. Skipping installation."
fi

echo "=========================================="
echo "Setup complete successfully!"
echo "=========================================="

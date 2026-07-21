#!/bin/sh
# =====================================================================
# Configuration Parameters for Database Download
# =====================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export FILE_ID="12c5Y6INCsb4TUmY2c_VRuGQgkHnkpFwp"
export DB_PATH="${SCRIPT_DIR}/db.sqlite3"
export DOWNLOAD_URL="https://drive.google.com/uc?export=download&id=${FILE_ID}"

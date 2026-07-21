# 002-bash-scripts: Windows 批次檔轉換 Linux Bash 腳本實作計畫

本文檔為 DjangoBlog 專案進行遠端 Linux 部署準備時，將 Windows 批次檔 (`.bat`) 轉換為 Linux Bash 腳本 (`.sh`) 之詳細步驟式實作計畫。

> [!NOTE]
> 依據需求，遠端 Linux 伺服器僅作為 Production/Staging 部署運行環境，不會進行 Git 版本 Commit 與 Push 作業，因此排除轉換 `setup_git.bat` ➔ `setup_git.sh`。

---

## 1. 轉換目標與需求概述

1. **跨平台與 Linux 相容性**：提供符合 POSIX / Bash 標準的腳本，確保在 Ubuntu/Debian/CentOS 等 Linux 遠端伺服器或 WSL 環境中能夠順暢執行。
2. **零程式碼改動**：本計畫僅針對環境配置與自動化腳本進行 Linux 版轉換，不修改 Django 專案內部 Python 程式碼或 HTML 模板。
3. **保持相容邏輯**：
   - 設定檔 `config.sh` 為全域下載變數中心。
   - `build_venv.sh` 自動建立虛擬環境並安裝 `requirement.txt`。
   - `download_db.sh` 自動下載 Google Drive 上的 `db.sqlite3`。

---

## 2. 步驟式實作計畫 (Step-by-Step Plan)

### Step 1: 建立通用設定腳本 `config.sh`
- **目的**：提供集中式參數設定（如資料庫下載連結與目標儲存路徑），供其他 Shell 腳本 `source` 載入。
- **實作細節**：
  - 使用 `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` 動態取得當前腳本所在的絕對路徑。
  - 設定 `FILE_ID="12c5Y6INCsb4TUmY2c_VRuGQgkHnkpFwp"`
  - 設定 `DB_PATH="${SCRIPT_DIR}/db.sqlite3"`
  - 設定 `DOWNLOAD_URL="https://drive.google.com/uc?export=download&id=${FILE_ID}"`
  - 使用 `export` 匯出變數以利子腳本存取。

### Step 2: 建立虛擬環境安裝腳本 `build_venv.sh`
- **目的**：在 Linux 環境中自動建立 Python 虛擬環境並安裝依賴。
- **實作細節**：
  - 檢查系統中是否存在 `python3`。
  - 若 `.venv` 目錄不存在，則執行 `python3 -m venv .venv`。
  - 升級 `pip`：`.venv/bin/python -m pip install --upgrade pip`。
  - 若 `requirement.txt` 存在，則執行 `.venv/bin/pip install -r requirement.txt`。
  - 加入明確的訊息輸出與錯誤捕捉 (`set -e` 或退出代碼 `exit 1`)。

### Step 3: 建立資料庫下載腳本 `download_db.sh`
- **目的**：從 Google Drive 自動下載開發與部署用之 `db.sqlite3` 資料庫。
- **實作細節**：
  - 先檢查並引用 `config.sh`（如 `source "${SCRIPT_DIR}/config.sh"`）。
  - 優先檢查並使用 `curl -L "$DOWNLOAD_URL" -o "$DB_PATH"`。
  - 若 `curl` 不存在，則退回使用 `wget -O "$DB_PATH" "$DOWNLOAD_URL"`。
  - 下載完畢後檢查檔案是否存在且大小大於 0，若失敗則回傳非 0 狀態碼。

### Step 4: 設定可執行權限與測試驗證
- **目的**：確保所有 `.sh` 檔案在 Linux 系統具備執行權限。
- **實作細節**：
  - 執行 `chmod +x config.sh build_venv.sh download_db.sh`。
  - 在 Linux/WSL 環境下測試依序執行各腳本。

---

## 3. 預計新增 Shell 腳本內容設計預覽 (Draft Specifications)

### 3.1 `config.sh` 設計預覽
```bash
#!/usr/bin/env bash
# =====================================================================
# Configuration Parameters for Database Download
# =====================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export FILE_ID="12c5Y6INCsb4TUmY2c_VRuGQgkHnkpFwp"
export DB_PATH="${SCRIPT_DIR}/db.sqlite3"
export DOWNLOAD_URL="https://drive.google.com/uc?export=download&id=${FILE_ID}"
```

### 3.2 `build_venv.sh` 設計預覽
```bash
#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Setting up Python Virtual Environment..."
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
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

# Upgrade pip
echo "Upgrading pip..."
"${SCRIPT_DIR}/.venv/bin/python" -m pip install --upgrade pip

# Install dependencies
if [ -f "${SCRIPT_DIR}/requirement.txt" ]; then
    echo "Installing dependencies from requirement.txt..."
    "${SCRIPT_DIR}/.venv/bin/pip" install -r "${SCRIPT_DIR}/requirement.txt"
else
    echo "[WARNING] requirement.txt not found. Skipping installation."
fi

echo "=========================================="
echo "Setup complete successfully!"
echo "=========================================="
```

### 3.3 `download_db.sh` 設計預覽
```bash
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
```

---

## 4. 後續執行與驗證檢查清單 (Verification Checklist)

- [ ] 1. 建立 3 個核心 `.sh` 檔案 (`config.sh`, `build_venv.sh`, `download_db.sh`) 於專案根目錄。
- [ ] 2. 賦予可執行權限：`chmod +x *.sh`。
- [ ] 3. 測試執行 `./build_venv.sh` 是否順利在 Linux 建立 `.venv` 並安裝 `Django` 與 `markdown`。
- [ ] 4. 測試執行 `./download_db.sh` 是否成功下載 `db.sqlite3`。

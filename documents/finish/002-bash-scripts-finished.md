# 002-bash-scripts: Windows 批次檔轉換 Linux Bash 腳本實作完成紀錄

本專案已完成 Linux 環境所需的 Shell 自動化腳本建立，並精準規範以 LF (`\n`) 格式換行，確保在遠端 Linux / WSL 環境下可直接執行。

---

## 1. 完成建立之檔案列表

| 檔名 | 路徑 | 功能說明 |
| --- | --- | --- |
| [config.sh](file:///c:/Users/admin/Desktop/2026-DjangoBlog/config.sh) | `/config.sh` | Linux 環境下載變數設定檔 (全域 `FILE_ID`, `DB_PATH`, `DOWNLOAD_URL`) |
| [build_venv.sh](file:///c:/Users/admin/Desktop/2026-DjangoBlog/build_venv.sh) | `/build_venv.sh` | 自動建立 Linux 虛擬環境 (`.venv/bin/python`)，升級 `pip` 並安裝 `requirement.txt` |
| [download_db.sh](file:///c:/Users/admin/Desktop/2026-DjangoBlog/download_db.sh) | `/download_db.sh` | 自動載入 `config.sh` 透過 `curl` / `wget` 下載遠端 `db.sqlite3` 資料庫 |

---

## 2. 核心特色與相容性處置

1. **Linux 換行字元 (LF) 轉換**：所有 `.sh` 檔案均經由 Unix 換行符號（`LF`）格式處理，避免出現 Windows `\r` 導致的 `\r: command not found` 錯誤。
2. **動態路徑解算**：使用 `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`，無論從何處呼叫腳本皆能正確定位專案根目錄。
3. **優化容錯與工具備援**：
   - `build_venv.sh` 檢查 `python3` 命令與 `.venv` 目錄狀態。
   - `download_db.sh` 支援 `curl` 與 `wget` 備援切換，並自動驗證下載完成度 (`-s`)。

---

## 3. Linux 伺服器部署執行步驟

登入遠端 Linux 伺服器並拉取專案後，依序執行：

```bash
# 1. 賦予可執行權限
chmod +x config.sh build_venv.sh download_db.sh

# 2. 建置虛擬環境與安裝依賴 (Django 6.0, markdown)
./build_venv.sh

# 3. 下載 SQLite 資料庫
./download_db.sh
```

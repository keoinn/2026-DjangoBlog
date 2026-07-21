# DjangoBlog 專案架構分析與 Linux 部署準備文檔

本文檔針對 **DjangoBlog** 專案進行全貌結構分析，並針對即將進行的遠端 Linux 環境部署，整理現有 Windows 批次檔 (`.bat`) 轉換至 Linux Shell 腳本 (`.sh`) 之對照與建議。

---

## 1. 專案整體架構概觀 (Project Overview)

DjangoBlog 是一個基於 Django 6.0 開發的現代化網誌系統，採用 Apple 風格深色毛玻璃 UI (Dark Glassmorphism) 設計，並支援所見即所得 (WYSIWYG) 的 Markdown 文章編輯與全站渲染。

### 核心技術棧 (Tech Stack)
- **後端框架**：Python 3.12+ / Django 6.0
- **Markdown 處理**：`markdown` 套件 (後端 Safe HTML 轉換 + 自訂 Template Filter `|markdown_to_html`)
- **前端編輯器**：EasyMDE (WYSIWYG Markdown 編輯器，整合於 `article/create.html`)
- **視覺與 UI**：Vanilla CSS / HTML5 (Apple 質感深色毛玻璃動態視覺，全域定義於 `templates/base.html`)
- **資料庫**：SQLite (`db.sqlite3`)，全站採用 Django ORM，具備無縫遷移至 MySQL / PostgreSQL 之能力。

---

## 2. 專案目錄與模組結構分析 (Directory Structure)

```text
2026-DjangoBlog/
├── DjangoBlog/               # Django 主專案設定目錄
│   ├── __init__.py
│   ├── asgi.py               # ASGI 非同步服務接口
│   ├── settings.py           # Django 全局配置 (DEBUG, ALLOWED_HOSTS, APPS, DB, TEMPLATES)
│   ├── urls.py               # 全局路由表 (Admin, 首頁, 文章模組, Auth)
│   └── wsgi.py               # WSGI 伺服器接口 (Linux Gunicorn / uWSGI 入口)
├── article/                  # 文章核心應用模組 (App)
│   ├── __init__.py
│   ├── admin.py              # 後台管理註冊
│   ├── apps.py               # App 設定
│   ├── forms.py              # 表單定義 (PostForm，整合 EasyMDE 相關元件)
│   ├── migrations/           # 資料庫遷移檔目錄
│   ├── models.py             # 資料模型 (Post: author, title, slug, content, pub_date)
│   ├── templatetags/         # 自訂 Django Template Tags/Filters
│   │   ├── __init__.py
│   │   └── custom_markdown.py# markdown_to_html 過濾器
│   ├── tests.py              # 單元測試
│   ├── urls.py               # 文章模組路由 (`/article/...`)
│   └── views.py              # 視圖邏輯 (index, create_post, user_login, user_logout)
├── templates/                # 前端模板 HTML 檔案
│   ├── base.html             # 基底頁面 (包含導覽列、全域 CSS 樣式、毛玻璃視覺)
│   ├── index.html            # 首頁與文章列表展示
│   ├── article/
│   │   └── create.html       # 發文頁面 (WYSIWYG Markdown 編輯器)
│   ├── components/           # 頁面元件 (如 header.html)
│   └── registration/
│       └── login.html        # 登入頁面
├── documents/                # 專案規劃與分析文檔
│   ├── 001-modules-plans.md   # 功能模組開發計畫
│   ├── finish/               # 已完成模組紀錄
│   └── project-arc.md        # 本專案架構分析與 Linux 轉移規劃文檔 (NEW)
├── build_venv.bat            # Windows: 建立 Python .venv 與安裝套件
├── config.bat                # Windows: 全局下載與 Git 設定變數
├── download_db.bat           # Windows: 從 Google Drive 下載 db.sqlite3
├── setup_git.bat             # Windows: 設定 Git 本地使用者
├── db.sqlite3                # 開發環境 SQLite 資料庫
├── manage.py                 # Django 管理工具腳本
├── Readme.md                 # 專案 Readme 檔
└── requirement.txt           # Python 依賴套件檔 (Django==6.0, markdown>=3.5)
```

---

## 3. Windows 批次檔對應 Linux 腳本轉換分析 (Linux Script Conversion Plan)

目前專案根目錄下存在 4 個 `.bat` 批次檔，主要用於 Windows 環境下的開發設置與資料庫下載。在轉移至 Linux 遠端伺服器時，只需將 3 個核心腳本 (`config.bat`, `build_venv.bat`, `download_db.bat`) 轉換為 Bash 腳本 (`.sh`)；而 `setup_git.bat` 無需轉換（因遠端伺服器僅作為部署運行環境，不會向 GitHub 推送程式碼版本資訊）：

### 3.1 `config.bat` ➔ `config.sh`
- **現有功能**：定義 `FILE_ID` (Google Drive)、`DB_PATH` 與 `DOWNLOAD_URL` 變數資訊。
- **Linux 轉換要點**：
  1. 使用 Shell 語法 `export VARIABLE="value"` 或單純 Shell 變數宣告。
  2. 動態取得當前腳本所在的絕對路徑：`DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
  3. `DB_PATH="$DIR/db.sqlite3"`。

### 3.2 `build_venv.bat` ➔ `build_venv.sh`
- **現有功能**：檢查 Python -> 建立 `.venv` 虛擬環境 -> 升級 `pip` -> 透過 `pip install -r requirement.txt` 安裝依賴。
- **Linux 轉換要點**：
  1. 檢查 `python3` 是否安裝。
  2. 使用 `python3 -m venv .venv` 建立虛擬環境 (伺服器需安裝 `python3-venv` 套件)。
  3. Linux 虛擬環境的可執行檔路徑為 `.venv/bin/python` 與 `.venv/bin/pip` (注意：Windows 為 `.venv\Scripts\...`)。
  4. 執行 `chmod +x build_venv.sh` 確保腳本具備可執行權限。

### 3.3 `download_db.bat` ➔ `download_db.sh`
- **現有功能**：引用 `config.bat`，透過 `curl.exe` 或 `powershell` 下載遠端 Google Drive 的 `db.sqlite3`。
- **Linux 轉換要點**：
  1. 透過 `source ./config.sh` 引入設定檔變數。
  2. 直接調用 Linux 原生 `curl -L "$DOWNLOAD_URL" -o "$DB_PATH"` 或 `wget -O "$DB_PATH" "$DOWNLOAD_URL"`。
  3. 驗證檔案下載成果並回傳對應的 exit status。

### 3.4 `setup_git.bat` (無需轉換)
- **說明**：遠端伺服器僅作為 Production/Staging 部署環境，不進行 Git 程式碼 Commit 與 Push 作業，故排除轉換 `setup_git.sh`。

---

## 4. 遠端 Linux 部署關鍵建議 (Linux Remote Deployment Recommendations)

1. **WSGI / Production 伺服器**：
   - 生產環境建議搭配 `gunicorn` (Python WSGI HTTP Server) 或 `uWSGI`，並使用 `Nginx` 作為反向代理 (Reverse Proxy) 處理靜態檔案與 SSL。
   - 可在 `requirement.txt` 新增 `gunicorn`。

2. **靜態檔案收集 (Static Files Collection)**：
   - 部署至 Linux 前或部署過程中，於 `settings.py` 設定 `STATIC_ROOT = BASE_DIR / 'staticfiles'`，並執行 `python manage.py collectstatic`。

3. **生產環境安全配置 (`settings.py`)**：
   - 將 `DEBUG = True` 改為經由環境變數讀取 (生產環境應為 `False`)。
   - `ALLOWED_HOSTS` 填入遠端伺服器之 Domain Name 或公網 IP。
   - `SECRET_KEY` 應改為從環境變數讀取，勿直接硬編碼於版本控制中。

4. **資料庫檔案權限 (Database File Permissions)**：
   - 若繼續在 Linux 使用 SQLite，需確保 Web 服務執行者 (如 `www-data` 或特定 deployment user) 對 `db.sqlite3` 檔案以及其所在目錄擁有**讀取與寫入**權限。

---

*備註：本分析報告未對任何專案原始碼進行修改，已精確留存於 `documents/project-arc.md` 供後續部署參考。*

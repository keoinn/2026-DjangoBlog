# 001-modules-plans: 文章發布與身份驗證功能實作計畫 (Markdown 專用)

本文檔為 DjangoBlog 專案「所見即所得 (WYSIWYG) Markdown 文章張貼介面」與「登入權限控制」功能之模組規劃與實作計畫。

---

## 1. 功能目標與需求概述

1. **必要登入驗證**：只有登入使用者才能存取發文介面並成功張貼文章。未登入者存取時重定向至登入頁。
2. **Markdown 儲存與 WYSIWYG 編輯介面**：
   - 後端資料庫 (`Post.content`) **純粹儲存原生 Markdown 格式文本**。
   - 前端發文介面提供「所見即所得 (WYSIWYG)」Markdown 編輯器（如 EasyMDE / Toast UI Editor），支援即時預視、快捷鍵與 Markdown 語法轉換。
3. **Markdown 模板渲染**：
   - 使用 Python 後端 Markdown 解析器（`markdown` 套件，支援代碼高亮與表格擴充）將 Markdown 轉為 HTML 於前端渲染，確保 SEO 友好與無樣式偏移。
4. **無縫整合現有視覺風格**：發文頁面與導覽列需符合專案現有的 Apple 深色質感 UI (Dark Glassmorphism Design)。
5. **資料庫相容性 (Future MySQL)**：繼續使用 Django ORM 抽象層，確保未來從 SQLite 遷移至 MySQL 時無須修改業務邏輯。

---

## 2. 模組變更與架構規劃

### 2.0 專案依賴套件 (Dependencies)
- **檔案**：`requirement.txt`
- **新增套件與版本資訊**：
  ```text
  Django==6.0
  markdown>=3.5
  ```
- **說明**：新增 `markdown>=3.5` 用於後端將 Markdown 格式的文字安全轉換解析為 HTML 供前端模板渲染。

### 2.1 資料模型 (Model Layer)
- **檔案**：`article/models.py`
- **變更**：
  - 為 `Post` 模型新增 `author` 外鍵 (指向 `django.contrib.auth.models.User`)。
  - `content` 欄位儲存原生 Markdown 字串。
  - 增加 `formatted_content` 屬性或使用 Template Filter，將 Markdown 自動轉換為 HTML 供前端輸出。
  - `slug` 欄位加入自動生成邏輯（如未填寫則依據標題或時間戳記自動產生）。

### 2.2 表單層 (Form Layer)
- **檔案**：`article/forms.py` [NEW]
- **變更**：
  - 建立 `PostForm` 繼承自 `forms.ModelForm`。
  - 包含 `title`、`slug` 與 `content` 欄位與驗證邏輯。

### 2.3 視圖與權限控制 (View & Auth Layer)
- **檔案**：`article/views.py`
- **變更**：
  - 實作 `create_post(request)` 視圖函式。
  - 使用 `@login_required(login_url='/accounts/login/')` 限制僅登入使用者可存取。
  - 實作 GET（渲染發文表單）與 POST（驗證並儲存 Markdown 文章）處理邏輯。
  - 整合或提供登入/登出視圖（`login_view` / `logout_view`）。

### 2.4 路由與 URL 配置 (Routing Layer)
- **檔案**：
  - `article/urls.py` [NEW]
  - `DjangoBlog/urls.py`
- **變更**：
  - 建立 `article/urls.py` 並定義 `path('create/', create_post, name='create_post')`。
  - 在 `DjangoBlog/urls.py` 引入 `article.urls` 及身份驗證路由 (`/accounts/login/`, `/accounts/logout/`)。

### 2.5 前端介面與模板 (Template & UI Layer)
- **檔案**：
  - `templates/article/create.html` [NEW]：發文頁面模板，繼承 `base.html`，引入 EasyMDE / Toast UI Editor (WYSIWYG Markdown)，套用深色模式表單樣式。
  - `article/templatetags/custom_markdown.py` [NEW]：自訂 Django Template Filter（`|markdown_to_html`），支援程式碼區塊高亮、表格與標籤安全渲染。
  - `templates/registration/login.html` [NEW]：登入頁面模板，質感深色卡片風格。
  - `templates/components/header.html` [MODIFY]：動態顯示導覽列按鈕：
    - 已登入：顯示「發表文章」、「用戶名稱」、「登出」。
    - 未登入：顯示「登入」。

---

## 3. 實作步驟流程

1. **Step 1: 安裝 Markdown 依賴與更新 Model & 資料庫遷移**
   - 擴充 `Post` model 加入 `author` 欄位。
   - 執行 `python manage.py makemigrations` 及 `python manage.py migrate`。

2. **Step 2: 建立表單與視圖 (Form & Views & Markdown Filter)**
   - 建立 `article/forms.py` 中的 `PostForm`。
   - 建立 `article/templatetags/custom_markdown.py` 轉換 Markdown 至 HTML。
   - 在 `article/views.py` 實作 `create_post` 視圖與登入/登出處理。

3. **Step 3: 設定 URL 路由**
   - 建立 `article/urls.py` 並更新主路由 `DjangoBlog/urls.py`。

4. **Step 4: 設計前端 GUI (WYSIWYG Markdown 編輯器與登入頁)**
   - 建立 `create.html` 並整合 EasyMDE (WYSIWYG Markdown) 富文本編輯器。
   - 建立 `login.html` 登入頁。
   - 更新 `header.html` 呈現登入狀態與「發表文章」入口。

5. **Step 5: 驗證與測試**
   - 驗證未登入使用者存取 `/article/create/` 是否正確跳轉至登入頁。
   - 驗證登入後透過 WYSIWYG Markdown 編輯器發布文章，資料庫是否精準儲存純 Markdown。
   - 驗證首頁與文章列表是否成功將 Markdown 轉換為 HTML 安全渲染。

---

## 4. 未來 MySQL 遷移準備與注意事項

- **ORM 規範**：所有資料庫操作皆透過 Django ORM (`Post.objects.create(...)`)。
- **切換 MySQL 步驟**：
  1. 安裝 MySQL 驅動（例如 `pymysql` 或 `mysqlclient`）。
  2. 於 `DjangoBlog/settings.py` 將 `DATABASES['default']` 引擎更換為 `django.db.backends.mysql` 並填寫主機與密碼配置。
  3. 執行 `python manage.py migrate` 即可無縫同步至 MySQL 資料庫。

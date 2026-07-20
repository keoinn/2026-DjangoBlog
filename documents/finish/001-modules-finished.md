# 001-modules-finished: 文章發布與身份驗證模組完成報告

本文件為 **DjangoBlog** 專案第一階段「所見即所得 (WYSIWYG) Markdown 文章張貼介面」與「登入權限控制」之模組完成總結與技術參考文檔，供接續任務之 AGENT 快速接軌與參考。

---

## 1. 階段概述 (Overview)

本階段完成了完整的文章發布流程與權限控制機制：
- **登入防護 (Auth Guard)**：限制只有登入使用者可進入 `/article/create/` 發布文章，未登入者會被自動重定向至 `/accounts/login/`。
- **Markdown 儲存**：資料庫 `Post.content` 欄位純粹儲存原生 Markdown 字串。
- **WYSIWYG Markdown 編輯器**：前端表單整合 EasyMDE 編輯器，提供「所見即所得」與 Markdown 雙向編輯介面。
- **後端安全轉譯**：建立 `custom_markdown` Template Filter，在前端渲染時將 Markdown 安全轉換為 HTML，並支援代碼區塊高亮、表格與標籤擴充。
- **自動化測試**：建立全套單元測試 (`article/tests.py`) 且已全部通過。

---

## 2. 變更與新增檔案列表 (Files Summary)

| 檔案路徑 | 變更類型 | 功能說明 |
| :--- | :--- | :--- |
| [`requirement.txt`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/requirement.txt) | **MODIFY** | 新增 `markdown>=3.5` 依賴套件。 |
| [`article/models.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/models.py) | **MODIFY** | `Post` 模型新增 `author` 外鍵 (指向 `User`)，並重寫 `save()` 自動處理 `slug` 生成。 |
| [`article/forms.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/forms.py) | **NEW** | `PostForm` (ModelForm)，含 `__init__` 處理隱藏 textarea 之 HTML5 `required` 屬性。 |
| [`article/templatetags/custom_markdown.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/templatetags/custom_markdown.py) | **NEW** | 自訂 Template Filter `markdown_to_html` 將 Markdown 轉為 HTML。 |
| [`article/views.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/views.py) | **MODIFY** | 實作 `@login_required` 的 `create_post` 視圖，以及 `user_login`、`user_logout` 視圖。 |
| [`article/urls.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/urls.py) | **NEW** | `article` 模組路由 (`path('create/', views.create_post, name='create_post')`)。 |
| [`DjangoBlog/urls.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/DjangoBlog/urls.py) | **MODIFY** | 引入 `article.urls` 及 `/accounts/login/`、`/accounts/logout/` 身份驗證路由。 |
| [`templates/article/create.html`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/templates/article/create.html) | **NEW** | 發文介面模板，整合 EasyMDE 編輯器與表單雙向同步腳本。 |
| [`templates/registration/login.html`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/templates/registration/login.html) | **NEW** | 登入頁面模板，採用 Apple 深色玻璃質感 UI。 |
| [`templates/components/header.html`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/templates/components/header.html) | **MODIFY** | 動態顯示「+ 發表文章」、用戶名稱與「登出 / 登入」狀態。 |
| [`templates/components/articles.html`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/templates/components/articles.html) | **MODIFY** | 以 `markdown_to_html` 轉譯文章內文並顯示作者資訊。 |
| [`article/tests.py`](file:///c:/Users/admin/Desktop/2026-DjangoBlog/article/tests.py) | **MODIFY** | 涵蓋權限攔截、Markdown 文章發布、與 HTML 轉譯之單元測試。 |

---

## 3. 重要技術細節與避坑指南 (Technical Gotchas)

1. **EasyMDE 與 HTML5 Form Validation 相容問題**：
   - **問題**：EasyMDE 在初始化時會將原有的 `<textarea>` 隱藏 (`display: none;`)。若 `<textarea>` 帶有 HTML5 原生 `required` 屬性，瀏覽器在 submit 時會拋出 `An invalid form control with name='content' is not focusable.` 錯誤並阻止發送。
   - **解決方案**：
     1. 在 `PostForm.__init__` 中使用 `self.fields['content'].widget.attrs.pop('required', None)` 移除前端原生 required 屬性（後端 `is_valid()` 依然保持驗證）。
     2. 在 `create.html` 中以 JS `form.addEventListener("submit", ...)` 手動校驗 EasyMDE 內容，若為空則引導焦點至編輯器，不為空則同步至原控制項發送。

2. **Slug 自動生成**：
   - `Post.save()` 中使用 `slugify(self.title, allow_unicode=True)` 處理中文標題。若結果仍為空，會以 `post-{timestamp}` 做 Fallback。

3. **單元測試驗證指令**：
   - 執行指令：`.venv\Scripts\python.exe manage.py test article`
   - 目前所有 3 項測試均通過（OK）。

---

## 4. 下階段 Agent 參考建議 (Next Steps & Context)

- **資料庫無縫遷移 (SQLite -> MySQL)**：
  - 現有模型皆標準使用 Django ORM。未來轉為 MySQL 時，只需在 `settings.py` 的 `DATABASES` 配置 MySQL 連線並安裝 `mysqlclient` / `PyMySQL` 即可，無需改動 models 或 views。
- **文章詳情頁 (Post Detail View)**：
  - 目前 `/` 首頁展示列表。後續若需要單篇文章獨立頁面，可以透過 `Post.slug` 或 `Post.id` 在 `article/urls.py` 中新增 `path('<slug:slug>/', views.post_detail, name='post_detail')`。
- **靜態檔案與 media 上傳擴充**：
  - 若未來發文介面需要支援直接上傳圖片至伺服器並嵌入 Markdown，可考慮擴充 EasyMDE 的 `imageUploadFunction` 並對接 Django 的 `FileField` 或圖片儲存視圖。

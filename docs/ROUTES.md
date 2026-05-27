# 路由設計文件 (ROUTES.md) - 自動打工排班系統

本文件詳細規劃了系統的 URL 路由、對應的 Jinja2 模板及邏輯功能。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/儀表板** | GET | `/` | `index.html` | 根據權限顯示店長或員工儀表板 |
| **登入頁面** | GET | `/login` | `login.html` | 顯示登入表單 |
| **執行登入** | POST | `/login` | — | 驗證身分並建立 Session |
| **登出** | GET | `/logout` | — | 清除 Session 並重導向至登入 |
| **自動排班頁面** | GET | `/scheduler` | `scheduler/index.html` | (店長專用) 顯示排班設定介面 |
| **執行自動排班** | POST | `/scheduler/run` | — | 執行演算邏輯，重導向至預覽頁 |
| **預覽班表** | GET | `/scheduler/preview`| `scheduler/preview.html` | 預覽產出的班表草稿 |
| **發布班表** | POST | `/scheduler/publish`| — | 正式發布班表並通知員工 |
| **請假申請頁面** | GET | `/leave` | `leave/apply.html` | (員工專用) 顯示請假表單 |
| **提交請假申請** | POST | `/leave/apply` | — | 儲存申請並通知店長 |
| **審核請假列表** | GET | `/admin/leaves` | `admin/leaves.html` | (店長專用) 顯示待審核請假清單 |
| **執行審核** | POST | `/admin/leaves/<id>/<status>`| — | 准駁請假申請 |

---

## 2. 路由詳細說明

### 2.1 主頁面 (main_routes)
- **處理邏輯**：檢查 `session['user_role']`，決定加載數據並渲染對應視圖。

### 2.2 認證模組 (auth_routes)
- **登入**：比對 `employees` 表中的 `password_hash`。
- **權限裝飾器**：實作 `@admin_required` 與 `@login_required` 確保安全性。

### 2.3 排班模組 (scheduler_routes)
- **Run**：呼叫 `app/models/schedule.py` 中的演算法。
- **Publish**：將 `shifts` 表中對應時段的 `status` 從 `draft` 更新為 `published`。

---

## 3. Jinja2 模板清單
- `base.html`: 包含導航欄與基礎封裝。
- `login.html`: 登入畫面。
- `index.html`: 主儀表板（含人力熱圖）。
- `scheduler/index.html`: 排班參數設定。
- `scheduler/preview.html`: 演算結果預覽。
- `leave/apply.html`: 員工請假表單。
- `admin/leaves.html`: 店長審核清單。

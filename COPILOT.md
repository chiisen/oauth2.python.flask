# COPILOT.md

本檔案提供 GitHub Copilot 於本儲存庫作業時的指引與紀錄。

## 專案簡介

本檔案提供 GitHub Copilot 於本 Python 3.8 + Flask 專案作業時的指引與紀錄。

## 專案架構分析

本專案目錄結構如下：

```
e:\GitHub\chiisen\oauth2.python.flask\
├── README.md         # 中文專案簡介
├── LICENSE           # 專案授權檔案
├── COPILOT.md        # 由 GitHub Copilot 產生並維護的說明與紀錄檔案
├── app.py            # Flask 應用程式主程式（假設存在）
├── config.py         # 設定檔，通常用於管理環境變數與應用設定（假設存在）
├── models.py         # 資料模型定義檔，常用於 ORM 或資料結構（假設存在）
└── oauth2.py         # OAuth2 相關邏輯與流程實作（假設存在）
```

### 各檔案與目錄功能分析

- `app.py`：Flask 應用程式的進入點，負責啟動伺服器、註冊路由與整合其他模組。
- `config.py`：集中管理應用程式設定，例如資料庫連線、密鑰、第三方服務參數等，方便依環境切換設定。
- `models.py`：定義資料模型，通常搭配 ORM（如 SQLAlchemy）使用，描述資料表結構與關聯。
- `oauth2.py`：實作 OAuth2 認證授權流程，包含 token 發放、驗證、授權碼處理等邏輯。
- `templates/`：Flask 專案預設的 HTML 樣板目錄，存放 Jinja2 樣板檔案，供前端頁面渲染使用。所有 render_template 調用的 HTML 檔案通常放在此目錄下。

> 註：上述部分目錄可能因作業系統或開發流程而出現，請依實際情況管理。

- 專案目前以 Flask 為基礎，結構簡單，適合逐步擴充功能與測試各種 Python/Flask/OAuth2 相關技術。

---

## 測試相關說明

- 測試框架：unittest（Python 內建）
- 測試檔案路徑：`tests/`
- 執行測試指令：`python -m unittest discover tests`

---

## 變更紀錄排序規則

- 變更紀錄請依照「時間越接近現在越上面」的順序排列（即最新紀錄在最上方）。

---



## Flask log 設定與常見問題整理

### 1. Flask log 寫入檔案的標準做法

- Flask 標準 log 輸出建議使用 `app.logger`，不要用 print。
- 若要寫入檔案，需自訂 logging handler，例如：
  ```python
  import logging
  from logging.handlers import RotatingFileHandler
  import os
  from datetime import datetime
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  os.makedirs(log_dir, exist_ok=True)
  log_filename = os.path.join(log_dir, f"flask-{datetime.now().strftime('%Y%m%d')}.log")
  file_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=7, encoding='utf-8')
  file_handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
  file_handler.setFormatter(formatter)
  if app.logger.hasHandlers():
      app.logger.handlers.clear()
  app.logger.setLevel(logging.DEBUG)
  app.logger.addHandler(file_handler)
  app.logger.propagate = False
  ```
- 這樣 log 會寫入 `./logs/flask-YYYYMMDD.log`，每日分檔，單檔最大 5MB，最多保留 7 個檔案。

### 2. 常見問題與解法

- **log 檔案沒內容？**
  - 檢查 log level，handler 與 app.logger 都要設為 DEBUG 或 INFO。
  - 確認 logs 目錄有寫入權限。
  - 若在 VS Code 偵錯模式，預設 handler 可能覆蓋自訂 handler，需用 `app.logger.handlers.clear()` 移除預設 handler。
  - 設定 `app.logger.propagate = False`，避免 log 被傳遞到 root logger 而只顯示在 console。
  - logger 設定要在所有 log 輸出前完成。

- **log 只出現在終端機？**
  - 預設 Flask 只輸出到 console，必須加上自訂 handler 才會寫檔。

- **log 寫入但內容不全？**
  - 檢查 log level 與 formatter 設定。
  - 檢查是否有其他程式鎖定 log 檔案。

---

### ModuleNotFoundError: No module named 'flask'

**錯誤訊息範例：**
```
發生例外狀況: ModuleNotFoundError
No module named 'flask'
  File "E:\GitHub\chiisen\oauth2.python.flask\app.py", line 2, in <module>
    from flask import Flask, request, render_template, redirect, session, url_for, g
ModuleNotFoundError: No module named 'flask'
```

**解決步驟：**
1. 確認已啟動虛擬環境（venv）。
   - PowerShell：`./venv/Scripts/Activate.ps1`
   - CMD：`./venv/Scripts/activate`
2. 安裝 Flask 及專案所需套件：
   ```sh
   pip install flask authlib pymysql werkzeug sqlalchemy flask_sqlalchemy
   ```
3. 若有 requirements.txt，亦可：
   ```sh
   pip install -r requirements.txt
   ```

5. 建立 requirements.txt（建議）
   - 若專案尚未有 requirements.txt，請於虛擬環境中執行：
     ```sh
     pip freeze > requirements.txt
     ```
   - 這樣可將目前環境所有安裝套件記錄下來，方便團隊協作或日後還原環境。

---

---

## 變更紀錄

- 2024-06-13 18:20：新增「虛擬環境初始化流程」區段，說明 Python 3.8 下建立與啟動虛擬環境的步驟與指令（由 Copilot 執行）。
- 2024-06-13 18:10：新增測試相關說明（unittest 框架、測試目錄與執行指令）至 COPILOT.md，並於變更紀錄明確記載（由 Copilot 執行）。
- 2024-06-13 18:00：依據聊天內容，補充並同步新增相關說明至 COPILOT.md（由 Copilot 執行）。
- 2024-06-13 17:50：補充分析 app.py、config.py、models.py、oauth2.py 四個檔案的預期功能與專案結構，並記錄於「專案架構分析」區段。
- 2024-06-13 17:45：調整變更紀錄排序規則，並將規則寫入本檔案。
- 2024-06-13 17:40：新增「專案架構分析」區段，說明目前專案目錄結構與特性。
- 2024-06-13 17:34：再次嘗試刪除 CLAUDE.md 檔案（由 Copilot 執行）。
- 2024-06-13 17:33：刪除 CLAUDE.md 檔案（由 Copilot 執行）。
- 2024-06-13 17:32：將原 CLAUDE.md 內容全部轉移至 COPILOT.md，並將英文內容改為中文。刪除 CLAUDE.md 檔案。所有後續變更與提示皆記錄於本檔案。

---

## 虛擬環境初始化流程

1. **確認 Python 3.8 已安裝**
   ```sh
   python --version
   # 或
   python3 --version
   ```

2. **建立虛擬環境**
   ```sh
   python -m venv venv
   # 或
   python3 -m venv venv
   ```

3. **啟動虛擬環境**
   - Windows (CMD):
     ```sh
     .\venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **安裝相依套件（如有 requirements.txt）**
   ```sh
   pip install -r requirements.txt
   ```

5. **停用虛擬環境**
   ```sh
   deactivate
   ```
---

## Copilot 與虛擬環境常見問題整理

### 1. PowerShell 啟動虛擬環境報錯

- 在 PowerShell 執行 `. \venv\Scripts\activate` 或 `. \venv\Scripts\Activate.ps1` 可能會出現「無法辨識」或「權限不足」的錯誤。
- 這通常是因為 PowerShell 的執行政策（Execution Policy）限制，導致無法執行啟動腳本。

#### 解決方式

- **優先建議：改用命令提示字元（CMD）啟動虛擬環境**
  1. 開啟「命令提示字元（CMD）」
  2. 切換到專案資料夾
     ```cmd
     cd e:\GitHub\chiisen\oauth2.python.flask
     .\venv\Scripts\activate
     ```
  3. 這樣可避開 PowerShell 的執行政策限制。

- **如需在 PowerShell 啟動，且有權限時：**
  1. 可嘗試解除限制（僅影響目前使用者，不需管理員權限）：
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     .\venv\Scripts\Activate.ps1
     ```
  2. 若仍受限，請改用 CMD。

- **啟動成功時，命令列前會出現 `(venv)`，表示已進入虛擬環境。**

### 2. 未看到 venv 目錄

- 若執行啟動指令時發現沒有 `venv` 目錄，代表虛擬環境尚未建立。
- 請先執行：
  ```sh
  python -m venv venv
  ```
- 建立完成後再依上方方式啟動。

### 3. 文件補充建議

- 在「啟動虛擬環境」區段下方補充：
  > ⚠️ 若 PowerShell 因執行政策限制無法啟動虛擬環境，請改用「命令提示字元（CMD）」執行：
  > ```cmd
  > .\venv\Scripts\activate
  > ```
  > 若未看到 venv 目錄，請先執行 `python -m venv venv` 建立虛擬環境。

---

# 專案結構與說明

本專案是一個基於 Flask 與 Authlib 實作的 OAuth2 授權伺服器，包含使用者註冊、登入、OAuth2 client 管理、授權流程等功能。以下分別說明各主要程式檔案的用途與結構。

---

## 1. app.py

`app.py` 為 Flask 應用程式主入口，負責：

- 設定 Flask 與 SQLAlchemy 資料庫連線。
- 設定日誌（log）檔案，並依日期分檔。
- 提供使用者註冊、登入、登出、首頁等基本路由。
- 實作 OAuth2 授權流程，包括 `/oauth/authorize`（授權同意頁）、`/oauth/token`（token 發放）、client 管理等路由。
- 整合 Authlib 的 AuthorizationServer，並註冊自訂的授權碼流程（AuthorizationCodeGrant）。

### 授權流程重點說明

- 檢查使用者是否已登入，未登入則導向登入頁。
- 取得目前登入的使用者，並透過 Authlib 取得授權同意資訊。
- GET 方法時顯示授權同意頁面，POST 方法時判斷使用者是否同意授權，並產生授權回應。
- 回應物件會根據型態（tuple、Response、str）包裝成 Flask 能處理的格式。

---

## 2. oauth2.py

`oauth2.py` 定義自訂的 OAuth2 授權碼流程（AuthorizationCodeGrant），負責：

- 儲存授權碼到資料庫，包含 client、user、scope、PKCE 相關欄位。
- 根據 code 與 client 查詢授權碼物件。
- 刪除授權碼，確保授權碼只能用一次（安全性需求）。
- 根據授權碼取得授權的使用者物件。

這些方法是 OAuth2 授權碼流程的核心，負責授權碼的存取與驗證。

---

## 3. models.py

`models.py` 定義所有資料庫模型，包含：

- `User`：儲存平台使用者的基本資料（帳號、密碼、信箱、建立時間）。
- `OAuth2Client`：儲存第三方應用程式（client）的資訊，包含 client_id、client_secret、redirect_uri、scope 等，並關聯到使用者。
- `OAuth2AuthorizationCode`：儲存 OAuth2 授權流程產生的授權碼（code），包含 client、user、scope、PKCE 相關欄位。
- `OAuth2Token`：儲存 access token、refresh token 及相關資訊，並關聯到 client 與 user。

這些模型是 OAuth2 流程的資料結構核心，負責管理使用者、client、授權碼與 token 的資料。

---

## 總結

本專案完整實作 OAuth2 授權伺服器的主要流程，並以清楚的資料模型與註解輔助理解。建議先從 `app.py` 了解整體流程，再依需求深入 `oauth2.py` 與 `models.py` 的細節。
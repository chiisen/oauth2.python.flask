# 🔐 oauth2.python.flask

使用 Python Flask 開發 OAuth2.0 測試範例 🚀

## 🌟 專案簡介
本專案是一個基於 **Flask** 與 **Authlib** 實作的 OAuth2 授權伺服器 🛡️。它展示了如何建立一個完整的 OAuth2 流程，包含使用者註冊、登入、Client 管理以及授權碼發放。

## 🏗️ 專案架構
本專案採用模組化設計，結構清晰：
- **`app.py`**: 應用程式核心，處理路由與 OAuth2 伺服器整合 🚪
- **`oauth2.py`**: 實作授權碼流程 (Authorization Code Grant) ⚙️
- **`models.py`**: 定義資料庫模型 (User, Client, Token) 📊
- **`config.py`**: 集中管理應用程式設定 🛠️

## 🚀 快速開始

### 1. 準備環境 💻
建議使用 Python 3.8+ 版本：
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境 (Windows)
.\venv\Scripts\activate
```

### 2. 安裝套件 📦
```bash
pip install -r requirements.txt
```

### 3. 執行程式 🔥
```bash
python src/app.py
```

## 🧪 測試與開發
執行以下指令進行單元測試：
```bash
python -m unittest discover tests
```

---
✨ 更多詳細文件請參閱 [COPILOT.md](./COPILOT.md)

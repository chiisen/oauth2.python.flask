# app.py


# 只保留必要初始化，route 匯入放在 app 定義之後
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from flask import Flask, session, g
from config import Config
from models import db, OAuth2Client, User
from authlib.integrations.flask_oauth2 import AuthorizationServer
from oauth2 import AuthorizationCodeGrant

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oauth2.db'  # 改用 SQLite 檔案，儲存在 ./instance 目錄下
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.secret_key = '3f87c95f63fa407b9d7d02e8a8b9456d8e1a3c313b24bcf0a4de76fe85868f20'  # 讓 session 正常運作

# 設定 log 檔案路徑與檔名（依日期分檔）
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"flask-{datetime.now().strftime('%Y%m%d')}.log")
# 設定 RotatingFileHandler，單檔最大 5MB，最多保留 7 個檔案
file_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=7, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
file_handler.setFormatter(formatter)
if app.logger.hasHandlers():
    app.logger.handlers.clear()
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.propagate = False

# 初始化 OAuth2 授權服務器
authorization = AuthorizationServer(
    app,
    query_client=lambda client_id: OAuth2Client.query.filter_by(client_id=client_id).first(),
    save_token=lambda _token, request: None  # 暫時不儲存 token，可以根據需求實現
)

# 註冊授權碼授權類型
authorization.register_grant(AuthorizationCodeGrant)

try:
    with app.app_context():
        db.create_all()
    app.logger.info("✅ 資料表已建立完成")
except Exception as e:
    app.logger.error("發生例外：%s", e, exc_info=True)

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = db.session.query(User).get(user_id) if user_id else None

@app.context_processor
def inject_user():
    return dict(user=g.user)

# 匯入路由處理函式
import route

# 註冊
@app.route("/register", methods=["GET", "POST"])
def register_view():
    return route.register()

# 登入
@app.route("/login", methods=["GET", "POST"])
def login_view():
    return route.login()

# 登出
@app.route("/logout")
def logout_view():
    return route.logout()

# 首頁
@app.route("/")
def home_view():
    return route.home()

# OAuth 授權
@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize_view():
    return route.authorize()

# OAuth token
@app.route('/oauth/token', methods=['POST'])
def issue_token_view():
    return route.issue_token()

# 客戶端列表
@app.route('/clients')
def list_clients_view():
    return route.list_clients()

# 新增客戶端
@app.route('/clients/new', methods=['GET', 'POST'])
def new_client_view():
    return route.new_client()

if __name__ == "__main__":
    try:
        # 啟動 Flask 應用程式
        app.run(debug=True)
    except Exception as e:
        app.logger.error(f"發生錯誤: {e}")


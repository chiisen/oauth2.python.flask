# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)

db = SQLAlchemy()

# 使用者模型，儲存平台使用者的基本資料
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 使用者唯一識別碼
    username = db.Column(db.String(40), unique=True, nullable=False)  # 使用者名稱，唯一且必填
    password_hash = db.Column(db.String(128), nullable=False)  # 密碼雜湊值，必填
    email = db.Column(db.String(100), unique=True, nullable=False)  # 電子郵件，唯一且必填
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間，預設為目前時間
    
    def __init__(self, username, email, password_hash, created_at=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        if created_at is not None:
            self.created_at = created_at

# OAuth2 Client 模型，儲存第三方應用程式（client）的資訊
class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'
    id = db.Column(db.Integer, primary_key=True)  # client 資料表主鍵
    # OAuth2ClientMixin 已經定義了 client_id, client_secret, client_name, redirect_uri, scope 等欄位
    # 所以這裡不需要重複定義
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # 關聯到使用者
    user = db.relationship('User')  # 取得 client 所屬的使用者物件

# OAuth2 授權碼模型，儲存授權流程產生的 code 及相關資訊
class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    code = db.Column(db.String(120), unique=True, nullable=False)  # 授權碼，唯一且必填
    client_id = db.Column(db.String(48))  # client_id
    redirect_uri = db.Column(db.Text)  # 重導 URI
    scope = db.Column(db.Text)  # 授權範圍
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # 關聯到使用者
    code_challenge = db.Column(db.String(128))  # PKCE code_challenge
    code_challenge_method = db.Column(db.String(10))  # PKCE code_challenge_method

# OAuth2 Token 模型，儲存 access token、refresh token 及相關資訊
class OAuth2Token(db.Model, OAuth2TokenMixin):
    ___tablename__ = 'oauth2_token'
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # 關聯到使用者
    user = db.relationship('User')  # 取得 token 所屬的使用者物件
    client_id = db.Column(db.String(48), db.ForeignKey('oauth2_client.client_id'))  # 關聯到 client
    client = db.relationship('OAuth2Client', backref='tokens')  # 取得 token 所屬的 client 物件

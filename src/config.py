import os

class Config:
    # 你的 Flask App Secret Key，用來加密 session 等資料，請換成安全隨機字串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uX7v0z@WRgJ3K$Yuj!p1NxL#5v9cm&d^KwTqA2HjRzGgU$PfNe#MEZhqyD!Xwb6P'

    # 資料庫連線字串，這裡示範 SQLite 連線
    # 格式: sqlite:///相對路徑或絕對路徑
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///./instance/oauth2.db'
    )

    # 設定是否追蹤修改 (不必要會有額外負擔，通常設False)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth2 Provider 相關設定（可依需求擴充）
    OAUTH2_REFRESH_TOKEN_GENERATOR = True

from flask import render_template, redirect, session, url_for, request, g, abort, make_response, Response
from models import db, User, OAuth2Client
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

from flask import current_app as app
from app import authorization

# 註冊
def register():
    error = None
    app.logger.info("進入註冊頁面")
    if request.method == "POST":
        app.logger.info(f"收到註冊請求: 使用者名稱={request.form.get('username')}, 電子郵件={request.form.get('email')}")
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        if not username or not email or not password:
            error = "所有欄位皆為必填"
            app.logger.warning("註冊失敗：有欄位未填寫 (Some fields are missing)")
        elif User.query.filter_by(username=username).first():
            error = "使用者名稱已被註冊"
            app.logger.warning(f"註冊失敗：使用者名稱已存在，名稱={username} (Username already exists)")
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_pw, created_at=datetime.utcnow())
            db.session.add(new_user)
            db.session.commit()
            app.logger.info(f"註冊成功：使用者名稱={username}, 電子郵件={email}")
            session["registered"] = True
            return redirect("/login")
    return render_template("register.html", error=error)

# 登入
def login():
    if "user_id" in session:
        app.logger.info(f"使用者已登入，使用者編號={session['user_id']}")
        return redirect(url_for("home_view"))
    error = None
    success_message = None
    if session.pop("registered", None):
        success_message = "註冊成功，請登入"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            app.logger.info(f"登入成功：使用者編號={user.id}，使用者名稱={username}")
            return redirect(url_for("home_view"))
        else:
            error = "帳號或密碼錯誤"
            app.logger.warning(f"登入失敗：使用者名稱={username} (Login failed)")
    return render_template("login.html", error=error, success_message=success_message)

# 登出
def logout():
    user_id = session.get("user_id")
    session.pop("user_id", None)
    app.logger.info(f"使用者登出：使用者編號={user_id}")
    return redirect("/login")

# 首頁
def home():
    if "user_id" not in session:
        app.logger.info("尚未登入，導向登入頁面 (Not logged in, redirect to login)")
        return redirect("/login")
    user = User.query.get(session["user_id"])
    if user:
        app.logger.info(f"進入首頁：使用者編號={user.id}")
    else:
        app.logger.warning("首頁載入失敗：找不到使用者 (User not found)")
        return redirect("/login")
    return render_template("home.html", user=user)

# OAuth 授權
def authorize():
    if 'user_id' not in session:
        app.logger.info(f"OAuth 授權頁面尚未登入，導向登入頁面，回原頁：{request.url}")
        return redirect('/login?next=' + request.url)
    user = User.query.get(session['user_id'])
    if user is None:
        app.logger.warning("OAuth 授權頁面載入失敗：找不到使用者 (User not found)")
        return redirect("/login")
    app.logger.info(f"進入 OAuth 授權頁面，使用者編號={user.id}")
    try:
        grant = authorization.get_consent_grant(end_user=user)
        app.logger.info(f"取得授權同意資訊成功：client_id={getattr(grant.client, 'client_id', None)}")
    except Exception as e:
        app.logger.error(f"取得授權同意資訊失敗：{e} (Error in consent grant)")
        return abort(400, description=f"授權請求無效：{e}")
    if request.method == 'GET':
        app.logger.info(f"顯示授權同意頁面：使用者編號={user.id}，client_id={getattr(grant.client, 'client_id', None)}")
        return render_template('authorize.html', user=user, grant=grant)
    if request.form.get('confirm'):
        app.logger.info(f"使用者同意授權：使用者編號={user.id}，client_id={getattr(grant.client, 'client_id', None)}")
        response = authorization.create_authorization_response(grant_user=user)
    else:
        app.logger.info(f"使用者拒絕授權：使用者編號={user.id}，client_id={getattr(grant.client, 'client_id', None)}")
        response = authorization.create_authorization_response(grant_user=None)
    if isinstance(response, tuple):
        resp, status, headers = response
        flask_response = make_response(resp, status)
        for header, value in headers:
            flask_response.headers[header] = value
        if not isinstance(flask_response, Response):
            flask_response = make_response(str(flask_response), status)
        return flask_response
    if isinstance(response, Response) or isinstance(response, str):
        return response
    return make_response(str(response), 200)

# OAuth token
def issue_token():
    app.logger.info("收到存取權杖 (token) 請求")
    response = authorization.create_token_response()
    from flask import make_response
    if isinstance(response, tuple):
        resp, status, headers = response
        flask_response = make_response(resp, status)
        for header, value in headers:
            flask_response.headers[header] = value
        return flask_response
    return response

# 客戶端列表
def list_clients():
    app.logger.info("查詢所有 OAuth2 客戶端 (client)")
    clients = OAuth2Client.query.all()
    return render_template('client_list.html', clients=clients)

# 新增客戶端
def new_client():
    if request.method == 'POST':
        app.logger.info("收到新增 OAuth2 客戶端 (client) 請求")
        user = User.query.first()
        if not user:
            app.logger.warning("新增客戶端失敗：找不到使用者 (User not found)")
            return "沒有找到使用者，請先註冊或登入", 400
        client_data = {
            'client_id': secrets.token_urlsafe(24),
            'client_secret': secrets.token_urlsafe(48),
            'client_name': request.form['client_name'],
            'redirect_uri': request.form['redirect_uri'],
            'scope': request.form['scope']
        }
        app.logger.info(f"建立客戶端：名稱={client_data['client_name']}，使用者編號={user.id}")
        client = OAuth2Client(**client_data)
        client.user_id = user.id
        db.session.add(client)
        db.session.commit()
        app.logger.info(f"客戶端新增成功：client_id={client.client_id}，使用者編號={user.id}")
        return redirect(url_for('list_clients_view'))
    app.logger.info("進入新增 OAuth2 客戶端頁面")
    return render_template('add_client.html')

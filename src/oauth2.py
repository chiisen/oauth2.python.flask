# oauth2.py
from authlib.oauth2.rfc6749 import grants
from models import db, User, OAuth2AuthorizationCode

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    # 儲存授權碼到資料庫
    def save_authorization_code(self, code_hash, request):
        # 建立新的授權碼物件
        auth_code = OAuth2AuthorizationCode()
        # 設定授權碼內容（加密後的 code）
        auth_code.code = code_hash
        # 設定 client_id（哪個 client 申請的）
        auth_code.client_id = request.client.client_id
        # 設定重導 URI（授權成功後導回哪裡）
        auth_code.redirect_uri = request.redirect_uri
        # 設定 scope（授權範圍）
        auth_code.scope = request.scope
        # 設定 user_id（哪個使用者授權的）
        auth_code.user_id = request.user.id
        # 設定 PKCE 相關欄位（如有）
        auth_code.code_challenge = request.data.get('code_challenge')
        auth_code.code_challenge_method = request.data.get('code_challenge_method')
        # 儲存到資料庫
        db.session.add(auth_code)
        db.session.commit()
        return auth_code

    # 根據 code 與 client 查詢授權碼
    def query_authorization_code(self, code, client):
        # 使用 getattr 函數來獲取 client_id 屬性，避免 Pylance 錯誤
        client_id = getattr(client, 'client_id', None)
        # 從資料庫查詢符合條件的授權碼
        return OAuth2AuthorizationCode.query.filter_by(code=code, client_id=client_id).first()

    # 刪除授權碼（用於授權碼兌換 access token 後，確保一次性使用）
    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    # 根據授權碼取得授權的使用者
    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)

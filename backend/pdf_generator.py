from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import requests

# 認証スコープを設定（ここでは Google Drive の読み取り権限）
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# トークンとクライアントシークレットのパス（backend フォルダ内に保存する）
# 認証情報のファイル
TOKEN_PATH = "backend/token.json"  # これはそのままでOK
CREDENTIALS_PATH = "backend/client_secret_330695572002-ao7iapnrsciesrj8u4dm85abduhuggic.apps.googleusercontent.com.json"

def generate_pdf(sheet_gid):
    """
    指定したシートの GID を使って、請求書スプレッドシートから PDF をダウンロードする関数
    
    ※ 請求書スプレッドシートのIDは固定でコード内にハードコードしています。
    """
    creds = None
    # 既存のトークンがあれば読み込む
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # 認証情報がない、もしくは無効な場合、新しく認証する
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    
    # 認証トークンをヘッダーに追加
    headers = {"Authorization": f"Bearer {creds.token}"}
    
    # 請求書スプレッドシートの ID（固定値）
    spreadsheet_id = "1ylFMe7tQQZzZRfok7Uv1Kp68sXfxeZk0sObDNm53EPs"
    # エクスポートURL（指定したシートのみPDF化）
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf&gid={sheet_gid}"
    
    # PDF のダウンロードリクエスト
    response = requests.get(export_url, headers=headers)
    
    pdf_filename = f"sheet_{sheet_gid}.pdf"
    if response.status_code == 200:
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"✅ {pdf_filename} をダウンロードしました！")
        return {"message": f"✅ {pdf_filename} をダウンロードしました！", "pdf_filename": pdf_filename}
    else:
        print(f"❌ ダウンロードに失敗しました: {response.status_code} {response.text}")
        return {"error": f"❌ ダウンロードに失敗しました: {response.status_code} {response.text}"}

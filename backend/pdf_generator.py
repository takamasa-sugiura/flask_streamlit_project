import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# スコープ設定
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

TOKEN_PATH = "backend/token.json"  # トークンは自動生成される
# CREDENTIALS_PATH は使わないので、代わりに環境変数を使用

# Render の環境変数から認証情報を取得
credentials_str = os.getenv("GOOGLE_CREDENTIALS")
if credentials_str is None:
    raise Exception("GOOGLE_CREDENTIALS 環境変数が設定されていません。")
credentials_json = json.loads(credentials_str)

# 認証情報の取得処理（トークンの生成）
creds = None
if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
    # 環境変数から直接認証情報を使用してフローを生成
    flow = InstalledAppFlow.from_client_config(credentials_json, SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as token_file:
        token_file.write(creds.to_json())

headers = {"Authorization": f"Bearer {creds.token}"}
spreadsheet_id = "1ylFMe7tQQZzZRfok7Uv1Kp68sXfxeZk0sObDNm53EPs"
# sheet_gid を後から引数で渡す前提
def generate_pdf(sheet_gid):
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf&gid={sheet_gid}"
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

import os
import json
import gspread
from google.oauth2.service_account import Credentials

# ✅ Google API 認証情報
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ 認証情報を `credentials.json` から取得
credentials_path = "backend/flask-sheets-project-1580c622794f"
if not os.path.exists(credentials_path):
    raise FileNotFoundError(f"❌ 認証ファイルが見つかりません: {credentials_path}")

creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
client = gspread.authorize(creds)

SPREADSHEET_ID = "1XOihFCwFJVyDZc2xW7N-hvXBKbi6xLwiG4T5zaKuT2E"  # ✅ あなたのスプレッドシート ID に変更

def edit_cell(sheet_name, cell, value):
    """ 指定したスプレッドシートのセルを編集する """
    try:
        print(f"📌 `/edit_cell` が呼ばれました！（{sheet_name}: {cell} → {value}）")
        
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(sheet_name)

        worksheet.update_acell(cell, value)

        return {"message": f"✅ セル {cell} を `{value}` に更新しました！"}

    except Exception as e:
        print(f"❌ `edit_cell` エラー: {str(e)}")
        return {"error": "セル編集に失敗しました", "details": str(e)}

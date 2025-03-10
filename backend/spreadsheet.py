import json
import os
import gspread
from google.oauth2.service_account import Credentials

# Google API 認証情報
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Render の環境変数から `credentials.json` を取得
credentials_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = Credentials.from_service_account_info(credentials_json, scopes=scope)
client = gspread.authorize(creds)


def edit_cell(spreadsheet_id, sheet_name, cell, value):
    try:
        print(f"📌 `/edit_cell` が呼ばれました！（{sheet_name}: {cell} → {value}）")
        
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        worksheet.update_acell(cell, value)

        return {"message": f"✅ セル {cell} を `{value}` に更新しました！"}

    except Exception as e:
        print(f"❌ `edit_cell` エラー: {str(e)}")
        return {"error": "セル編集に失敗しました", "details": str(e)}

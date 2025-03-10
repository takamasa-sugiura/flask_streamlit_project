import json
import os
import gspread
from google.oauth2.service_account import Credentials

# Google API 認証情報
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Render の環境変数から `credentials.json` を取得
credentials_str = os.getenv("GOOGLE_CREDENTIALS")

# ✅ デバッグ用にログを出力（Render の Logs に表示される）
if credentials_str is None:
    print("❌ `GOOGLE_CREDENTIALS` の環境変数が設定されていません！")
else:
    print("✅ `GOOGLE_CREDENTIALS` を取得しました！")

# JSON をロード
credentials_json = json.loads(credentials_str)
creds = Credentials.from_service_account_info(credentials_json, scopes=scope)
client = gspread.authorize(creds)


SPREADSHEET_ID = "1XOihFCwFJVyDZc2xW7N-hvXBKbi6xLwiG4T5zaKuT2E"  # ✅ あなたのスプレッドシート ID に変更

def edit_cell(spreadsheet_id, sheet_name, cell, value):
    """ 指定したスプレッドシートのセルを編集する """
    try:
        print(f"📌 `/edit_cell` が呼ばれました！（{spreadsheet_id} - {sheet_name}: {cell} → {value}）")
        
        # ✅ `spreadsheet_id` を使ってスプレッドシートを開く
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        worksheet.update_acell(cell, value)

        return {"message": f"✅ セル {cell} を `{value}` に更新しました！"}

    except Exception as e:
        print(f"❌ `edit_cell` エラー: {str(e)}")
        return {"error": "セル編集に失敗しました", "details": str(e)}

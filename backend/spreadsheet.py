import gspread
import os
from google.oauth2.service_account import Credentials

# Google API 認証情報
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 既存の `credentials.json` を使う
creds = Credentials.from_service_account_file("backend/credentials.json", scopes=scope)
client = gspread.authorize(creds)

def copy_sheet(month):
    spreadsheet_id = "1ylFMe7tQQZzZRfok7Uv1Kp68sXfxeZk0sObDNm53EPs"  # ✅ 以前のスプレッドシートID
    spreadsheet = client.open_by_key(spreadsheet_id)
    original_sheet = spreadsheet.worksheet("杉浦さん2025/〇月度請求書(原本)")  # ✅ コピー元のシート名

    # **新しいシート名を決定**
    new_sheet_name = f"杉浦さん2025/{month}月度請求書test"

    # **請求書のシートを複製**
    new_sheet = spreadsheet.duplicate_sheet(original_sheet.id, new_sheet_name=new_sheet_name)

    return {
        "message": f"✅ {new_sheet_name} を作成しました！",
        "sheet_id": new_sheet.id
    }

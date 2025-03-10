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




#ここより上は各種インポートとJSONのロードのため共通これより下を編集して機能を編集する


def copy_and_update():
    """
    請求書スプレッドシート（A）の原本シートを複製し、
    加入者一覧スプレッドシート（B）の指定セル（J1）の値を取得して、
    複製したシートの指定範囲（B13:D14）に貼り付ける。
    """
    # スプレッドシート A（請求書）の ID（固定値）
    spreadsheet_a = client.open_by_key("1ylFMe7tQQZzZRfok7Uv1Kp68sXfxeZk0sObDNm53EPs")
    
    # スプレッドシート B（加入者一覧）の ID（固定値）
    spreadsheet_b = client.open_by_key("1BVjrK-Q1jH8klurJmh4bMkQ1ILtKtA2qutZ6ataoIdM")
    
    # 請求書の原本シートを取得（コピー元）
    original_sheet = spreadsheet_a.worksheet("杉浦さん2025/〇月度請求書(原本)")
    
    # 複製した後の新しいシート名を決定
    new_sheet_name = "杉浦さん2025/2月度請求書テスト"
    
    # 原本シートを複製し、新しいシートを作成
    new_sheet = spreadsheet_a.duplicate_sheet(original_sheet.id, new_sheet_name=new_sheet_name)
    new_sheet_gid = new_sheet.id  # 新しいシートのID（gid）
    print(f"✅ シート '{original_sheet.title}' を複製し、新しいシート '{new_sheet_name}' (GID: {new_sheet_gid}) を作成しました！")
    
    # 加入者一覧スプレッドシートからコピー元ワークシートを取得
    source_sheet = spreadsheet_b.worksheet("2025/2")
    
    # 例として、セル J1 の値を取得
    cell_value = source_sheet.acell("J1").value
    print(f"📋 コピー元のセル J1 の値: {cell_value}")
    
    # 複製したシートを取得して、指定したセル範囲に値を貼り付け（書式維持）
    target_sheet = spreadsheet_a.worksheet(new_sheet_name)
    target_sheet.update(values=[[cell_value]], range_name="B13:D14", value_input_option="USER_ENTERED")
    print(f"✅ {cell_value} を B13:D14 に貼り付けました！（書式維持）")
    
    return {
        "message": f"✅ {new_sheet_name} を作成し、加入者一覧のセル J1 の値 ({cell_value}) を B13:D14 に貼り付けました！",
        "sheet_id": new_sheet.id
    }

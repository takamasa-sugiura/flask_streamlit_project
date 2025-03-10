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

from flask import Flask, jsonify, request
from backend import spreadsheet  # `spreadsheet.py` をインポート

# Flask アプリの作成
app = Flask(__name__)

# ✅ ルート `/` → アプリが動いているか確認するためのエンドポイント
@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask!"})

# ✅ `/edit_cell` → Google スプレッドシートの特定のセルを編集するエンドポイント
@app.route("/edit_cell", methods=["POST"])
def edit_cell():
    try:
        # クライアントからのリクエスト JSON を取得
        data = request.json

        # 必要なパラメータがすべて含まれているか確認
        required_keys = ["spreadsheet_id", "sheet_name", "cell", "value"]
        if not all(key in data for key in required_keys):
            return jsonify({"error": "必要なパラメータが不足しています"}), 400

        # スプレッドシートを編集する処理を呼び出し
        result = spreadsheet.edit_cell(
            data["spreadsheet_id"], 
            data["sheet_name"], 
            data["cell"], 
            data["value"]
        )

        return jsonify(result)

    except Exception as e:
        print(f"❌ `/edit_cell` エラー: {str(e)}")
        return jsonify({"error": "セル編集に失敗しました", "details": str(e)}), 500

# ✅ Flask アプリを起動
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # `Render` でデフォルトポートを設定
    app.run(host="0.0.0.0", port=port, debug=True)

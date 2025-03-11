from flask import Flask, jsonify, request
from backend import spreadsheet  # `spreadsheet.py` をインポート
from backend import pdf_generator

# ✅ Flask アプリの作成
app = Flask(__name__)

# ✅ ルート `/` → アプリの動作確認用
@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask!"})

@app.route("/copy_sheet", methods=["POST"])
def copy_sheet():
    try:
        data = request.get_json(force=True)
        # 必要なパラメータは省略しているので、固定で実行する例
        result = spreadsheet.copy_and_update()
        return jsonify(result)
    except Exception as e:
        print(f"❌ `/copy_sheet` エラー: {str(e)}")
        return jsonify({"error": "シートコピーに失敗しました", "details": str(e)}), 500

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf_endpoint():
    try:
        data = request.get_json(force=True)
        if "sheet_gid" not in data:
            return jsonify({"error": "sheet_gid パラメータが必要です"}), 400
        
        result = pdf_generator.generate_pdf(data["sheet_gid"])
        return jsonify(result)
    except Exception as e:
        print(f"❌ `/generate_pdf` エラー: {str(e)}")
        return jsonify({"error": "PDF生成に失敗しました", "details": str(e)}), 500
    
# ✅ Flask アプリを起動
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # `Render` でデフォルトポートを設定
    app.run(host="0.0.0.0", port=port, debug=True)

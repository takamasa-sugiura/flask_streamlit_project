from flask import Flask, jsonify, request
from backend import spreadsheet  # `spreadsheet.py` をインポート

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask!"})

@app.route("/copy_sheet", methods=["POST"])
def copy_sheet():
    try:
        data = request.json
        if "month" not in data:
            return jsonify({"error": "month パラメータが必要です"}), 400
        
        result = spreadsheet.copy_sheet(data["month"])
        return jsonify(result)

    except Exception as e:
        print(f"❌ `/copy_sheet` エラー: {str(e)}")
        return jsonify({"error": "シートコピーに失敗しました", "details": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

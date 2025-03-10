from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello, Flask!"})

@app.route("/ping")
def ping():
    return jsonify({"message": "pong!"})

@app.route("/users", methods=["GET"])
def get_users():
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    return jsonify(users)

@app.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"received": data})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

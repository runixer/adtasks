from flask import Flask, request, jsonify

app = Flask(__name__)

current_flag = ''

@app.route('/put_flag', methods=['POST'])
def put_flag():
    data = request.json
    if type(data) != dict or "flag" not in data:
        return jsonify({"ok": False, "error": "invalid request"})
    global current_flag
    current_flag = data["flag"]
    return jsonify({"ok": True})

@app.route('/get_flag', methods=['POST'])
def get_flag():
    return jsonify({"ok": True, "flag": current_flag})

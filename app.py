from flask import Flask, render_template, request, jsonify
from utils import load_memory, add_memory, context, add_history

app = Flask(__name__)

load_memory()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("q")

    ans = context(q)
    add_history(q, ans)

    return jsonify({"a": ans})

@app.route("/teach", methods=["POST"])
def teach():
    q = request.json.get("q")
    a = request.json.get("a")

    add_memory(q, a)

    return jsonify({"msg": "শিখে ফেলেছি 😎"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

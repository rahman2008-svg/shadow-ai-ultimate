from flask import Flask, render_template, request, jsonify
from utils import load_big_knowledge, find_best_answer, auto_learn, add_memory
import os

app = Flask(__name__)
load_big_knowledge()

# Home page: split UI for Ask + Teach
@app.route("/")
def index():
    return render_template("index.html")

# Ask route
@app.route("/ask", methods=["POST"])
def ask():
    q = request.form.get("question", "").strip()
    ans = find_best_answer(q)
    auto_learn(q, ans)  # auto-learn from chat
    return jsonify({"answer": ans})

# Teach route
@app.route("/teach", methods=["POST"])
def teach():
    q = request.form.get("question", "").strip()
    a = request.form.get("answer", "").strip()
    add_memory(q, a)
    return jsonify({"status": "ok", "message": "Knowledge added!"})

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    app.run(host="0.0.0.0", port=8000, debug=True)

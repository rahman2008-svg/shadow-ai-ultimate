from flask import Flask, render_template, request, jsonify
from utils import load_memories, load_big_knowledge, find_best_answer, auto_learn

app = Flask(__name__)

# 🔥 Load memories + big knowledge
load_memories()
load_big_knowledge()

# 🌟 Home redirects to chat
@app.route("/")
def home():
    return render_template("chat.html")

# 🌟 Teach page
@app.route("/teach")
def teach_page():
    return render_template("teach.html")

# 🌟 Teach route
@app.route("/teach_submit", methods=["POST"])
def teach_submit():
    q = request.form.get("question")
    a = request.form.get("answer")
    auto_learn(q, a)
    return jsonify({"status": "success", "message": "Saved successfully!"})

# 🌟 Ask route
@app.route("/ask", methods=["POST"])
def ask():
    q = request.form.get("question")
    ans = find_best_answer(q)
    auto_learn(q, ans)
    return jsonify({"answer": ans})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

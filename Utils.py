# utils.py
import os
import json
import random
from rapidfuzz import fuzz

# -----------------------------
# Config
MEMORY_FOLDER = "data"
MAX_PER_FILE = 5000

# -----------------------------
# In-memory storage
memories = []
token_map = {}  # word -> list of memories
big_knowledge = []

# -----------------------------
# Helper functions
def normalize(text):
    return text.lower().strip()

# -----------------------------
# Load big knowledge
def load_big_knowledge():
    global big_knowledge
    try:
        with open(os.path.join(MEMORY_FOLDER, "big_knowledge.json"), encoding="utf-8") as f:
            text = f.read().strip()
            if text.startswith("["):
                big_knowledge = json.loads(text)
            else:
                big_knowledge = [json.loads(line) for line in text.splitlines() if line.strip()]
        print(f"Loaded {len(big_knowledge)} Q&A from big_knowledge.json")
    except Exception as e:
        print("Error loading big_knowledge.json:", e)
        big_knowledge = []

# -----------------------------
# Add memory
def add_memory(question, answer):
    global memories
    if len(question) < 3 or len(answer) < 3:
        return
    memories.append({"question": question, "answer": answer})
    
    # Update token map for faster search
    for word in set(normalize(question).split()):
        token_map.setdefault(word, []).append({"question": question, "answer": answer})
    
    # Save to last memory file
    files = sorted([f for f in os.listdir(MEMORY_FOLDER) if f.startswith("memory_") and f.endswith(".json")])
    last_file = os.path.join(MEMORY_FOLDER, files[-1]) if files else os.path.join(MEMORY_FOLDER, "memory_1.json")

    try:
        with open(last_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append({"question": question, "answer": answer})
            if len(data) > MAX_PER_FILE:
                # Split memory (optional)
                new_file = os.path.join(MEMORY_FOLDER, f"memory_{len(files)+1}.json")
                with open(new_file, "w", encoding="utf-8") as nf:
                    nf.write(json.dumps(data[MAX_PER_FILE:], ensure_ascii=False, indent=2))
                data = data[:MAX_PER_FILE]
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()
    except Exception as e:
        print("Error saving memory:", e)

# -----------------------------
# Auto-learn (teach from chat)
def auto_learn(q, a):
    add_memory(q, a)

# -----------------------------
# Generate smart human-style answer
def generate_smart_answer(raw_answer):
    if not raw_answer:
        return "আমি এখনো শিখছি। দয়া করে teach করো।"

    templates = [
        f"{raw_answer}",
        f"{raw_answer}।",
        f"উত্তর: {raw_answer}",
        f"এটার উত্তর হলো {raw_answer}",
        f"তথ্য অনুযায়ী {raw_answer}",
        f"আমি যা জানি, {raw_answer}"
    ]
    return random.choice(templates)

# -----------------------------
# Find best answer from memory + big knowledge
def find_best_answer(question):
    qn = normalize(question)
    words = set(qn.split())
    candidates = []

    # Search token map
    for word in words:
        if word in token_map:
            candidates.extend(token_map[word])

    # fallback: last 500 memories
    if not candidates:
        candidates = memories[-500:]

    best = None
    score_max = 0

    # Check big knowledge first
    for item in big_knowledge:
        score = fuzz.token_set_ratio(qn, normalize(item['question']))
        if score > score_max:
            score_max = score
            best = item['answer']

    # Check memory
    for item in candidates:
        score = fuzz.token_set_ratio(qn, normalize(item['question']))
        if score > score_max:
            score_max = score
            best = item['answer']

    return generate_smart_answer(best)

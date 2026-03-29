import os, json
from rapidfuzz import fuzz

MEMORY_FILE = "data/memory.json"
MAX_PER_FILE = 10000

# In-memory storage
memories = []
big_knowledge = []

# 🔥 Load memories
def load_memories():
    global memories
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                memories = json.load(f)
            except:
                memories = []

# 🔥 Save memory
def add_memory(q, a):
    global memories
    memories.append({"question": q, "answer": a})
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

# 🔥 Load big knowledge
def load_big_knowledge():
    global big_knowledge
    if os.path.exists("data/big_knowledge.json"):
        with open("data/big_knowledge.json", encoding="utf-8") as f:
            try:
                big_knowledge = json.load(f)
            except:
                big_knowledge = []

# 🔥 Normalize string
def normalize(text):
    return text.lower().strip()

# 🔥 Find best answer
def find_best_answer(qn):
    q = normalize(qn)
    # 1️⃣ Check big knowledge first
    score_max = 0
    best = None
    for item in big_knowledge:
        score = fuzz.token_set_ratio(q, normalize(item['question']))
        if score > score_max:
            score_max = score
            best = item['answer']

    # 2️⃣ Check memories
    for item in memories[-500:]:
        score = fuzz.token_set_ratio(q, normalize(item['question']))
        if score > score_max:
            score_max = score
            best = item['answer']

    if score_max >= 60:
        return f"{best}"
    return "আমি এখনো শিখছি। দয়া করে teach করো।"

# 🔥 Auto learn
def auto_learn(q, a):
    if len(q) > 5 and len(a) > 5:
        add_memory(q, a)

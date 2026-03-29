import os, json, random
from rapidfuzz import fuzz

DATA_FOLDER = "data"

memories = []
token_map = {}
chat_history = []

def normalize(text):
    return text.lower().strip()

def load_memory():
    global memories
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    memories.clear()

    for f in os.listdir(DATA_FOLDER):
        if f.endswith(".json"):
            with open(os.path.join(DATA_FOLDER, f), encoding="utf-8") as file:
                memories.extend(json.load(file))

    build_index()

def build_index():
    global token_map
    token_map = {}
    for item in memories:
        for w in set(normalize(item['question']).split()):
            token_map.setdefault(w, []).append(item)

def add_memory(q, a):
    memories.append({"question": q, "answer": a})

    file = os.path.join(DATA_FOLDER, "memory.json")
    data = []
    if os.path.exists(file):
        data = json.load(open(file, encoding="utf-8"))

    data.append({"question": q, "answer": a})
    json.dump(data, open(file, "w", encoding="utf-8"), ensure_ascii=False)

def smart_answer(ans):
    if not ans:
        return random.choice([
            "আমি এখনও শিখছি 🙂",
            "এটা জানি না, আমাকে শেখাও 😅",
            "আরও তথ্য দিলে বুঝতে পারবো 🤔"
        ])

    return random.choice([
        ans,
        "উত্তর: " + ans,
        "আমি জানি " + ans
    ])

def search(q):
    qn = normalize(q)
    words = set(qn.split())

    candidates = []
    for w in words:
        if w in token_map:
            candidates += token_map[w]

    if not candidates:
        candidates = memories[-100:]

    best, score = None, 0

    for item in candidates:
        s = fuzz.token_set_ratio(qn, normalize(item['question']))
        if s > score:
            score = s
            best = item['answer']

    if score > 60:
        return smart_answer(best)

    return smart_answer(None)

def context(q):
    if any(x in q for x in ["এটা","ওটা","এর","তার","this","that"]):
        if chat_history:
            return "আগের তথ্য অনুযায়ী: " + chat_history[-1][1]

    return search(q)

def add_history(q, a):
    chat_history.append((q,a))
    if len(chat_history) > 5:
        chat_history.pop(0)

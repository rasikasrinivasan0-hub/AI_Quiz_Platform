import json
import random
import os

def generate_quiz(subject, difficulty):

    filename = subject.lower().replace(" ", "_") + ".json"
    file_path = os.path.join("data", filename)

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtered = [q for q in data if q["difficulty"] == difficulty]

    random.shuffle(filtered)

    return filtered[:20]
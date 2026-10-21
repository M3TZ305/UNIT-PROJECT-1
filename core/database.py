import json
import os

DB_FILE = "data_store.json"

DEFAULT_AGENTS = [
    {"id": "01", "name": "DeepCode-V4", "specialty": "Architecture", "success_rate": 99.4, "price": 450, "stock": 10},
    {"id": "02", "name": "SecGuard-X", "specialty": "Cyber Defense", "success_rate": 98.8, "price": 600, "stock": 5},
    {"id": "03", "name": "DataVision-Pro", "specialty": "Analytics", "success_rate": 97.2, "price": 350, "stock": 8},
    {"id": "04", "name": "NeuralWriter", "specialty": "Content Generation", "success_rate": 95.5, "price": 250, "stock": 15}
]

def load_data():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "agents": DEFAULT_AGENTS,
            "cart": [],
            "history": [],
            "tokens": 2000,
            "theme": "Cyberpunk Neon"
        }
        save_data(initial_data)
        return initial_data
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "theme" not in data:
                data["theme"] = "Cyberpunk Neon"
            return data
    except:
        return {"agents": DEFAULT_AGENTS, "cart": [], "history": [], "tokens": 2000, "theme": "Cyberpunk Neon"}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

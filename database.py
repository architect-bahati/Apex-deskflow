import json
import os

DATA_FILE = "data.json"

def load_data():
    """Loads transactions and tasks from a local JSON database file."""
    if not os.path.exists(DATA_FILE):
        return {"transactions": [], "tasks": []}
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {"transactions": [], "tasks": []}

def save_data(data):
    """Saves updated transactions and tasks back to the database file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False
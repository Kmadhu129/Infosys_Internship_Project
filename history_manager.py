import json
import uuid
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("chat_history.json")


def _read():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_history():
    return _read()


def save_history(history):
    _write(history)


def new_chat():
    history = _read()
    chat_id = str(uuid.uuid4())

    chat = {
        "id": chat_id,
        "title": "New Chat",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": []
    }

    history.insert(0, chat)
    _write(history)
    return chat_id


def delete_chat(chat_id):
    history = _read()
    history = [c for c in history if c["id"] != chat_id]
    _write(history)

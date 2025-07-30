# services/trello_service.py

import os
import requests
import json

KEY   = os.environ.get("TRELLO_KEY")
TOKEN = os.environ.get("TRELLO_TOKEN")
BOARD = os.environ.get("BOARD_ID")  # optional: scope to a board

if not KEY or not TOKEN:
    raise RuntimeError("TRELLO_KEY and TRELLO_TOKEN must be set in your .env")

def _load_local_tasks():
    """
    Load tasks from local fallback file task_data.json
    """
    try:
        with open("task_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        # ensure shape: list of dicts with id, name, (optional) effort
        return [{'id': d['id'], 'name': d['name'], 'effort': d.get('effort', 0)} for d in data]
    except Exception as e:
        print(f"[Fallback Error] Could not load task_data.json: {e}")
        return []

def fetch_tasks_from_trello():
    """
    Fetch tasks (Trello cards) from Trello API.
    Falls back to local task_data.json on any error.
    """
    if BOARD:
        url = f"https://api.trello.com/1/boards/{BOARD}/cards?key={KEY}&token={TOKEN}"
    else:
        url = f"https://api.trello.com/1/members/me/cards?key={KEY}&token={TOKEN}"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        cards = resp.json()
        print(f"[Trello] Loaded {len(cards)} cards from Trello")
        return [{'id': c['id'], 'name': c['name'], 'effort': 0} for c in cards]

    except requests.RequestException as err:
        print(f"[Trello API Error] {err} — falling back to task_data.json")
        return _load_local_tasks()

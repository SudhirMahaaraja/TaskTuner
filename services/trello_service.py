import os, requests, json

KEY     = os.environ.get("TRELLO_KEY")
TOKEN   = os.environ.get("TRELLO_TOKEN")
BOARD_ID= os.environ.get("BOARD_ID")

if not KEY or not TOKEN:
    raise RuntimeError("Set TRELLO_KEY and TRELLO_TOKEN in .env")
if not BOARD_ID:
    raise RuntimeError("Set BOARD_ID in .env")

def fetch_tasks_from_trello():
    url = (f"https://api.trello.com/1/boards/{BOARD_ID}/cards"
           f"?key={KEY}&token={TOKEN}")
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        cards = resp.json()
        print(f"[Trello] Loaded {len(cards)} cards from board {BOARD_ID}")
        return [{'id': c['id'], 'name': c['name']} for c in cards]

    except requests.HTTPError as http_err:
        print(f"[Trello API Error] {http_err} — falling back to sample_data.json")
        with open("sample_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[Fallback] Loaded {len(data)} mock tasks")
        return data

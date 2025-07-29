import json, threading
STORE_FILE = 'tasks_store.json'
_STORE_LOCK = threading.Lock()

class Task:
    _store = {}

    def __init__(self, id, name, effort=0):
        self.id = id; self.name = name; self.effort = effort

    @classmethod
    def _load_store(cls):
        try:
            with open(STORE_FILE) as f:
                data = json.load(f)
            cls._store = {d['id']: Task(d['id'], d['name'], d['effort']) for d in data}
        except FileNotFoundError:
            cls._store = {}

    @classmethod
    def _save_store(cls):
        with _STORE_LOCK:
            with open(STORE_FILE, 'w') as f:
                json.dump([t.to_dict() for t in cls._store.values()], f, indent=2)

    @classmethod
    def from_dict(cls, d):
        return cls(d['id'], d['name'], d.get('effort', 0))

    @classmethod
    def get(cls, task_id):
        return cls._store.get(task_id)

    def save(self):
        Task._store[self.id] = self
        Task._save_store()

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'effort': self.effort}

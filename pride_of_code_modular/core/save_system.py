import json, os
from typing import Dict, Any
from config import SAVE_VERSION

class SaveSystem:
    def __init__(self, path='save.json'):
        self.path = path

    def save(self, data: Dict[str, Any]):
        payload = {'_version': SAVE_VERSION, 'data': data}
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
        ver = payload.get('_version', 1)
        return payload.get('data', {})

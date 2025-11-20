from typing import Dict, Any

class Achievements:
    def __init__(self):
        self.achievements: Dict[str, Dict[str, Any]] = {}

    def register(self, key, name, description):
        self.achievements[key] = {'name':name,'description':description,'unlocked':False}

    def unlock(self, key):
        if key in self.achievements:
            self.achievements[key]['unlocked'] = True

    def get_unlocked(self):
        return [k for k,v in self.achievements.items() if v['unlocked']]

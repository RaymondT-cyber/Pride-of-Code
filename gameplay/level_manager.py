from typing import Dict, Any
from .validators import BaseValidator, Week1Validator

class LevelManager:
    def __init__(self):
        # simple registry mapping level id to validator and metadata
        self.levels: Dict[str, Dict[str, Any]] = {}
        self.register('week1', {'title':'Week 1 - Lists', 'validator': Week1Validator()})

    def register(self, id, meta):
        self.levels[id] = meta

    def get_level(self, id):
        return self.levels.get(id)

    def validate(self, id, code_globals):
        meta = self.get_level(id)
        if not meta:
            return False, 'Unknown level'
        validator: BaseValidator = meta.get('validator')
        if not validator:
            return False, 'No validator'
        return validator.validate(code_globals)

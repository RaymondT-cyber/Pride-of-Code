# Simple validators for levels. Each validator accepts execution namespace (globals) and returns (ok, message)
from typing import Tuple, Any

class BaseValidator:
    def validate(self, ns: dict) -> Tuple[bool, str]:
        raise NotImplementedError()

class Week1Validator(BaseValidator):
    def validate(self, ns: dict):
        # expect a list named 'brass_section' of length >=3
        val = ns.get('brass_section')
        if isinstance(val, list) and len(val) >= 3:
            return True, 'Good job - found brass_section'
        return False, 'Please create list named brass_section with at least 3 items'

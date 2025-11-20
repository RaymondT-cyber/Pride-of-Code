from typing import Dict, Any

class State:
    def enter(self, **params): pass
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface): pass
    def handle_event(self, ev): pass

class StateManager:
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.current: State | None = None
        self.current_name: str | None = None

    def register(self, name: str, state: State):
        self.states[name] = state

    def switch(self, name: str, **params):
        if self.current:
            try: self.current.exit()
            except Exception: pass
        self.current = self.states.get(name)
        self.current_name = name
        if self.current:
            try: self.current.enter(**params)
            except Exception: pass

    def update(self, dt: float):
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)

    def handle_event(self, ev):
        if self.current:
            self.current.handle_event(ev)

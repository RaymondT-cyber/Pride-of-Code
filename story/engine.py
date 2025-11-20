import json, pygame
from typing import List, Dict, Any

class StoryEngine:
    def __init__(self):
        self.chapters: List[Dict[str, Any]] = []
        self.index = 0
        self.font = pygame.font.SysFont('arial', 20)

    def load(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.chapters = data.get('chapters', [])
        self.index = 0

    def next(self):
        if self.index < len(self.chapters)-1:
            self.index += 1

    def update(self, dt):
        pass

    def draw(self, surface):
        if not self.chapters: return
        chap = self.chapters[self.index]
        surface.fill((10,10,10))
        text = chap.get('text','')
        y = 60
        lines = text.split('\n')
        for line in lines:
            s = self.font.render(line, True, (240,240,240))
            surface.blit(s, (60, y)); y += self.font.get_linesize()

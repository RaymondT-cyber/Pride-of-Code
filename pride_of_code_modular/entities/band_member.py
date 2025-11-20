import pygame
from typing import Tuple

class BandMember(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int,int], color=(255,200,0)):
        super().__init__()
        self.x, self.y = pos
        self.color = color
        self.image = pygame.Surface((24,40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self._draw_body()

    def _draw_body(self):
        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, self.color, (6,10,12,20))
        pygame.draw.circle(self.image, (30,30,30), (12,6), 6)

    def update(self, dt: float):
        # placeholder for animation / movement
        pass
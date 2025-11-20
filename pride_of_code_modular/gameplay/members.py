import pygame
class BandMember(pygame.sprite.Sprite):
    def __init__(self, pos, skin=None):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.Surface((24,40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.skin = skin or {'color':(200,180,60)}
        self._draw()

    def _draw(self):
        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, self.skin['color'], (6,10,12,20))
        pygame.draw.circle(self.image, (40,40,40), (12,6), 6)

    def update(self, dt):
        pass

import pygame, random, math
from typing import Tuple

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int,int], color: Tuple[int,int,int], lifetime:int=40, ptype:str="burst"):
        super().__init__()
        self.x, self.y = pos
        self.ptype = ptype
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(3,7)
        # velocity
        if ptype == "burst":
            self.vx = random.uniform(-3,3)
            self.vy = random.uniform(-6,-2)
        elif ptype == "sparkle":
            angle = random.uniform(0, 2*math.pi)
            s = random.uniform(1,3)
            self.vx = math.cos(angle)*s
            self.vy = math.sin(angle)*s
        else:
            self.vx = random.uniform(-1,1)
            self.vy = random.uniform(-2,0)

        # create a small surface for sprite (we'll scale on draw)
        size_px = max(8, self.size*2)
        self.image = pygame.Surface((size_px, size_px), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self._update_image()

    def _update_image(self):
        self.image.fill((0,0,0,0))
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        s = int(self.size * max(1.0, self.lifetime/self.max_lifetime))
        pygame.draw.circle(self.image, (*self.color, alpha), (self.image.get_width()//2, self.image.get_height()//2), max(1, s))

    def update(self, dt: float = 1.0):
        # dt is seconds
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        if self.ptype == "burst":
            self.vy += 0.3 * dt * 60
        elif self.ptype == "sparkle":
            self.vx *= 0.98
            self.vy *= 0.98

        self.lifetime -= max(1, int(dt*60))
        if self.lifetime <= 0:
            self.kill()
            return

        self.rect.center = (int(self.x), int(self.y))
        self._update_image()
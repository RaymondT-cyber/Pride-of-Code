import pygame, random, math
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color=(255,220,80), vel=None, lifetime=60):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel if vel is not None else (random.uniform(-2,2), random.uniform(-5,-1)))
        self.lifetime = lifetime
        self.max_life = lifetime
        size = random.randint(3,6)
        self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size, size), size)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def update(self, dt):
        # dt is seconds
        self.vel.y += 9.8 * dt  # gravity
        self.pos += self.vel * (dt*60)
        self.lifetime -= max(1, int(dt*60))
        if self.lifetime <= 0:
            self.kill()
            return
        self.rect.center = (int(self.pos.x), int(self.pos.y))

import pygame
class Panel:
    def __init__(self, rect, color=(30,30,30), border=True):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.border = border

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.border:
            pygame.draw.rect(surface, (255,255,255), self.rect, 1)

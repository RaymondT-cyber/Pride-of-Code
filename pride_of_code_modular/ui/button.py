import pygame
from typing import Callable, Tuple

class Button:
    def __init__(self, rect: pygame.Rect, text: str, onclick: Callable=None, font=None):
        self.rect = rect
        self.text = text
        self.onclick = onclick
        self.font = font or pygame.font.SysFont('arial', 20)
        self.hover = False

    def draw(self, surf):
        color = (100,200,100) if not self.hover else (140,230,140)
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, (0,0,0))
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(ev.pos)
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos) and self.onclick:
                self.onclick()
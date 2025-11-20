import pygame
from core.state_manager import State

class ResultsScene(State):
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.font = pygame.font.SysFont('arial', 24)

    def enter(self, **params):
        self.message = params.get('message', 'Results')

    def draw(self, surface):
        surface.fill((40,30,40))
        txt = self.font.render(self.message, True, (240,240,240))
        surface.blit(txt, (60,60))

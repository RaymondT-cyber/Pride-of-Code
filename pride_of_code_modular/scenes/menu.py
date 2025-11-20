import pygame
from core.state_manager import State

class MainMenu(State):
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.title_font = pygame.font.SysFont('arial', 40)
        self.small = pygame.font.SysFont('arial', 20)
        self.buttons = []

    def enter(self, **params):
        pass

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
            # quick start to level select
            self.manager.switch('level_select')

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((20,30,50))
        txt = self.title_font.render('Pride of Code', True, (240,240,240))
        surface.blit(txt, (60,60))
        info = self.small.render('Press Enter to go to Level Select', True, (200,200,200))
        surface.blit(info, (60,140))

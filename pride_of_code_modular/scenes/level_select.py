import pygame
from core.state_manager import State

class LevelSelect(State):
    def __init__(self, manager, game, level_manager):
        self.manager = manager
        self.game = game
        self.level_manager = level_manager
        self.font = pygame.font.SysFont('arial', 24)

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.manager.switch('menu')

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_1:
            # start level 1 in editor scene
            self.manager.switch('editor', level_id='week1')

    def draw(self, surface):
        surface.fill((30,40,60))
        header = self.font.render('Level Select (press 1 to start Week1)', True, (240,240,240))
        surface.blit(header, (40,60))

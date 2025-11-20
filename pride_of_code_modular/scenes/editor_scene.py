import pygame
from core.state_manager import State

class EditorScene(State):
    def __init__(self, manager, game, level_manager):
        self.manager = manager
        self.game = game
        self.level_manager = level_manager
        self.font = pygame.font.SysFont('arial', 20)
        # Editor is provided by game.editor (in core game)
    def enter(self, **params):
        self.level_id = params.get('level_id', None)
        self.level_data = self.level_manager.get_level(self.level_id) if self.level_id else None

    def handle_event(self, ev):
        # editor handles input; allow ESC to go back
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.manager.switch('level_select')

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((50,70,50))
        title = self.font.render(f'Editor - {self.level_id}', True, (255,255,255))
        surface.blit(title, (20,20))
        # assume game.editor exists and draw it on right side
        if hasattr(self.game, 'editor'):
            self.game.editor.draw(surface)

import pygame
from core.state_manager import State
from story.engine import StoryEngine

class StoryScene(State):
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        self.engine = StoryEngine()

    def enter(self, **params):
        story_file = params.get('story_file')
        if story_file:
            self.engine.load(story_file)

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.engine.next()

    def update(self, dt):
        self.engine.update(dt)

    def draw(self, surface):
        surface.fill((10,10,10))
        self.engine.draw(surface)

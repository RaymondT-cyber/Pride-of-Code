import pygame
import time

from config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE

from core.state_manager import StateManager
from core.audio_manager import AudioManager
from core.save_system import SaveSystem

from gameplay.level_manager import LevelManager
from ui.editor import CodeEditor

from scenes.menu import MainMenu
from scenes.level_select import LevelSelect
from scenes.editor_scene import EditorScene
from scenes.results import ResultsScene
from scenes.story import StoryScene


class PrideOfCodeGame:
    def __init__(self):
        # -------------------------------
        # Window
        # -------------------------------
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # -------------------------------
        # Time management
        # -------------------------------
        self.clock = pygame.time.Clock()
        self.last_time = time.time()

        # -------------------------------
        # Systems
        # -------------------------------
        self.audio = AudioManager()
        self.save = SaveSystem()
        self.level_manager = LevelManager()

        # -------------------------------
        # Editor (global instance)
        # -------------------------------
        # IMPORTANT: you can reposition or resize this panel later
        self.editor = CodeEditor(
            x=400, 
            y=80, 
            width=WINDOW_WIDTH - 420, 
            height=WINDOW_HEIGHT - 160
        )

        # -------------------------------
        # State Manager + Scene Registration
        # -------------------------------
        self.state_manager = StateManager()

        # Menu
        self.state_manager.register("menu", 
            MainMenu(self.state_manager, self))

        # Level Select
        self.state_manager.register("level_select",
            LevelSelect(self.state_manager, self, self.level_manager))

        # Editor Scene
        self.state_manager.register("editor",
            EditorScene(self.state_manager, self, self.level_manager))

        # Results Scene
        self.state_manager.register("results",
            ResultsScene(self.state_manager, self))

        # Story Scene
        self.state_manager.register("story",
            StoryScene(self.state_manager, self))

        # Begin in main menu
        self.state_manager.switch("menu")

    # -------------------------------------------------
    # Main Game Loop
    # -------------------------------------------------
    def run(self):
        running = True

        while running:
            # --------------------------
            # Delta-time calculation
            # --------------------------
            now = time.time()
            dt = now - self.last_time
            self.last_time = now

            # --------------------------
            # Event Handling
            # --------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    # Editor gets first chance when active scene is editor
                    if self.state_manager.current_name == "editor":
                        self.editor.handle_event(event)

                    self.state_manager.handle_event(event)

            # --------------------------
            # Update
            # --------------------------
            self.state_manager.update(dt)

            # --------------------------
            # Draw
            # --------------------------
            self.screen.fill((20, 20, 30))    # global background
            self.state_manager.draw(self.screen)
            pygame.display.flip()

            # --------------------------
            # Framerate cap
            # --------------------------
            self.clock.tick(60)

"""Enhanced Main Menu with Retro Bowl aesthetic."""

import pygame
from core.state_manager import State
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_BLUE, COLOR_GOLD, COLOR_TEXT
from ui.retro_button import RetroButton


class RetroMainMenu(State):
    """Main menu with Retro Bowl-inspired design."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        
        # Fonts
        self.font_title = pygame.font.SysFont('arial', 56, bold=True)
        self.font_subtitle = pygame.font.SysFont('arial', 24)
        self.font_small = pygame.font.SysFont('arial', 16)
        
        # Buttons
        button_width = 300
        button_height = 60
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        start_y = 280
        spacing = 80
        
        self.buttons = [
            RetroButton(button_x, start_y, button_width, button_height, 
                       "START CAMPAIGN", COLOR_BLUE),
            RetroButton(button_x, start_y + spacing, button_width, button_height,
                       "SANDBOX MODE", COLOR_BLUE),
            RetroButton(button_x, start_y + spacing * 2, button_width, button_height,
                       "QUIT", (100, 40, 40))
        ]
        
        # Animation
        self.title_pulse = 0
        
    def enter(self, **params):
        """Called when entering this state."""
        pass
        
    def handle_event(self, ev):
        """Handle input events."""
        for i, button in enumerate(self.buttons):
            if button.handle_event(ev):
                if i == 0:  # Campaign
                    self.manager.switch('enhanced_editor', level_id='week1_lesson1')
                elif i == 1:  # Sandbox
                    self.manager.switch('enhanced_editor', level_id='sandbox')
                elif i == 2:  # Quit
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    
    def update(self, dt):
        """Update animation."""
        self.title_pulse += dt * 2
        
    def draw(self, surface):
        """Render the menu."""
        # Background gradient effect (simple)
        surface.fill(COLOR_BG)
        
        # Draw subtle grid pattern
        for x in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(surface, (30, 30, 40), (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(surface, (30, 30, 40), (0, y), (WINDOW_WIDTH, y), 1)
            
        # Title with animation
        import math
        pulse = int(abs(math.sin(self.title_pulse) * 10))
        
        # Shadow
        title_shadow = self.font_title.render('CODE OF PRIDE', True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 4, 104))
        surface.blit(title_shadow, shadow_rect)
        
        # Main title (with pulse)
        title = self.font_title.render('CODE OF PRIDE', True, COLOR_GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        surface.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_subtitle.render('Pride of Casa Grande Marching Band', True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 160))
        surface.blit(subtitle, subtitle_rect)
        
        # School colors banner
        banner_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, 190, 400, 6)
        pygame.draw.rect(surface, COLOR_BLUE, banner_rect.inflate(0, 0))
        pygame.draw.rect(surface, COLOR_GOLD, banner_rect.inflate(0, -6).move(0, 9))
        
        # Tagline
        tagline = self.font_small.render('Learn Python Through Marching Band', True, (180, 180, 180))
        tagline_rect = tagline.get_rect(center=(WINDOW_WIDTH // 2, 220))
        surface.blit(tagline, tagline_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Footer
        footer = self.font_small.render('v1.0 | An Educational Coding Game', True, (100, 100, 100))
        footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        surface.blit(footer, footer_rect)
        
        # Pixel art decorations (simple marchers)
        self._draw_pixel_marcher(surface, 100, 400, COLOR_BLUE)
        self._draw_pixel_marcher(surface, WINDOW_WIDTH - 100, 400, COLOR_GOLD)
        
    def _draw_pixel_marcher(self, surface, x, y, color):
        """Draw a simple pixel art marcher decoration."""
        # Head
        pygame.draw.rect(surface, (220, 200, 180), (x - 6, y - 20, 12, 12))
        # Body
        pygame.draw.rect(surface, color, (x - 8, y - 6, 16, 20))
        # Legs
        pygame.draw.rect(surface, (60, 60, 80), (x - 8, y + 14, 6, 12))
        pygame.draw.rect(surface, (60, 60, 80), (x + 2, y + 14, 6, 12))
        # Instrument (simplified)
        pygame.draw.circle(surface, COLOR_GOLD, (x + 12, y), 6)
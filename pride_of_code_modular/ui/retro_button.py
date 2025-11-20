"""Retro-style UI buttons matching Retro Bowl aesthetic."""

import pygame
from config import COLOR_BLUE, COLOR_GOLD, COLOR_TEXT


class RetroButton:
    """A retro-styled button with pixel art aesthetic."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, color=None, text_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color or COLOR_BLUE
        self.text_color = text_color or COLOR_TEXT
        self.hover_color = COLOR_GOLD
        self.is_hovered = False
        self.is_pressed = False
        
        self.font = pygame.font.SysFont('arial', 18, bold=True)
        
    def handle_event(self, event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered:
                self.is_pressed = False
                return True
            self.is_pressed = False
            
        return False
        
    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        # Determine color based on state
        if self.is_pressed:
            color = (self.color[0] - 30, self.color[1] - 30, self.color[2] - 30)
            offset = 2
        elif self.is_hovered:
            color = self.hover_color
            offset = 0
        else:
            color = self.color
            offset = 0
            
        # Draw button with retro style
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect)
        
        # Main button
        button_rect = self.rect.copy()
        button_rect.y += offset
        pygame.draw.rect(surface, color, button_rect)
        pygame.draw.rect(surface, COLOR_TEXT, button_rect, 2)
        
        # Highlight (top-left)
        pygame.draw.line(surface, (255, 255, 255), 
                        (button_rect.left + 2, button_rect.top + 2),
                        (button_rect.right - 2, button_rect.top + 2), 1)
        pygame.draw.line(surface, (255, 255, 255),
                        (button_rect.left + 2, button_rect.top + 2),
                        (button_rect.left + 2, button_rect.bottom - 2), 1)
        
        # Text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        surface.blit(text_surf, text_rect)
        
    def set_text(self, text: str):
        """Update button text."""
        self.text = text
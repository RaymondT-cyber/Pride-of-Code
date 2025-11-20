"""
Main Menu - Retro-style menu for Code of Pride.

This module provides a retro-style main menu with pixel art aesthetics
that matches the overall game theme.
"""

import pygame
import math
from typing import List, Tuple, Callable
from config import COLOR_BLUE, COLOR_GOLD, COLOR_BG, COLOR_TEXT, WINDOW_WIDTH, WINDOW_HEIGHT


class RetroButton:
    """A retro-style button with pixel art aesthetics."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 callback: Callable = None, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = font or pygame.font.SysFont('arial', 18, bold=True)
        self.hovered = False
        self.pressed = False
        
        # Colors
        self.colors = {
            'normal_bg': (50, 50, 70),
            'hover_bg': (70, 70, 100),
            'pressed_bg': (40, 40, 60),
            'border': COLOR_BLUE,
            'text': COLOR_TEXT,
            'text_hover': COLOR_GOLD
        }
        
    def handle_event(self, event) -> bool:
        """Handle pygame events for this button.
        
        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return False  # Don't trigger on press
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    self.callback()
                return True  # Button was clicked
            self.pressed = False
        return False
        
    def draw(self, surface: pygame.Surface):
        """Draw the button on the given surface."""
        # Determine colors based on state
        if self.pressed:
            bg_color = self.colors['pressed_bg']
            text_color = self.colors['text']
        elif self.hovered:
            bg_color = self.colors['hover_bg']
            text_color = self.colors['text_hover']
        else:
            bg_color = self.colors['normal_bg']
            text_color = self.colors['text']
            
        # Draw background
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, self.colors['border'], self.rect, 2)
        
        # Draw text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def set_position(self, x: int, y: int):
        """Set the button position."""
        self.rect.x = x
        self.rect.y = y


class RetroMainMenu:
    """Main menu with retro pixel art aesthetics."""
    
    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
        # Font setup
        self.title_font = pygame.font.SysFont('arial', 48, bold=True)
        self.subtitle_font = pygame.font.SysFont('arial', 24)
        self.button_font = pygame.font.SysFont('arial', 20, bold=True)
        
        # Create buttons
        button_width = 300
        button_height = 50
        start_y = self.height // 2 - 50
        
        self.buttons: List[RetroButton] = [
            RetroButton(
                self.width // 2 - button_width // 2, start_y, 
                button_width, button_height, "Campaign Mode",
                font=self.button_font
            ),
            RetroButton(
                self.width // 2 - button_width // 2, start_y + 70, 
                button_width, button_height, "Challenge Mode",
                font=self.button_font
            ),
            RetroButton(
                self.width // 2 - button_width // 2, start_y + 140, 
                button_width, button_height, "Sandbox Mode",
                font=self.button_font
            ),
            RetroButton(
                self.width // 2 - button_width // 2, start_y + 210, 
                button_width, button_height, "Settings",
                font=self.button_font
            )
        ]
        
        # Colors
        self.colors = {
            'background': COLOR_BG,
            'title': COLOR_GOLD,
            'subtitle': (200, 200, 200),
            'border': COLOR_BLUE
        }
        
        # Animation
        self.title_bounce = 0
        self.title_direction = 1
        
    def handle_event(self, event) -> str:
        """Handle pygame events for the menu.
        
        Returns:
            String indicating which menu option was selected, or None
        """
        for button in self.buttons:
            if button.handle_event(event):
                # Return the button text as the selection
                return button.text.lower().replace(' ', '_')
        return None
        
    def update(self, dt: float):
        """Update menu animations.
        
        Args:
            dt: Delta time in seconds
        """
        # Animate title
        self.title_bounce += dt * 2 * self.title_direction
        if self.title_bounce > 1:
            self.title_bounce = 1
            self.title_direction = -1
        elif self.title_bounce < 0:
            self.title_bounce = 0
            self.title_direction = 1
            
    def draw(self, surface: pygame.Surface):
        """Draw the main menu.
        
        Args:
            surface: Surface to draw on
        """
        # Draw background
        surface.fill(self.colors['background'])
        
        # Draw decorative border
        border_rect = pygame.Rect(20, 20, self.width - 40, self.height - 40)
        pygame.draw.rect(surface, self.colors['border'], border_rect, 3)
        
        # Draw title with animation
        title_text = "CODE OF PRIDE"
        title_surf = self.title_font.render(title_text, True, self.colors['title'])
        title_y_offset = int(10 * abs(math.sin(self.title_bounce * math.pi)))
        surface.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 
                                 80 + title_y_offset))
        
        # Draw subtitle
        subtitle_text = "A Python Marching Band Adventure"
        subtitle_surf = self.subtitle_font.render(subtitle_text, True, self.colors['subtitle'])
        surface.blit(subtitle_surf, (self.width // 2 - subtitle_surf.get_width() // 2, 150))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
            
        # Draw footer
        footer_text = "Use mouse to navigate | Click to select"
        footer_surf = self.subtitle_font.render(footer_text, True, (150, 150, 150))
        surface.blit(footer_surf, (self.width // 2 - footer_surf.get_width() // 2, 
                                  self.height - 50))
        
    def resize(self, width: int, height: int):
        """Handle window resize.
        
        Args:
            width: New window width
            height: New window height
        """
        self.width = width
        self.height = height
        
        # Reposition buttons
        button_width = 300
        button_height = 50
        start_y = self.height // 2 - 50
        
        positions = [
            (self.width // 2 - button_width // 2, start_y),
            (self.width // 2 - button_width // 2, start_y + 70),
            (self.width // 2 - button_width // 2, start_y + 140),
            (self.width // 2 - button_width // 2, start_y + 210)
        ]
        
        for i, button in enumerate(self.buttons):
            button.set_position(positions[i][0], positions[i][1])
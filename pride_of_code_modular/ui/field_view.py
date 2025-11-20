"""
Field View - Retro Bowl-style marching field simulator.

This module renders the football field and animates band members
in a classic 8-bit pixel art style.
"""

import pygame
import math
from typing import List, Tuple, Optional
from config import (
    FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT, FIELD_OFFSET_X, FIELD_OFFSET_Y,
    COLOR_FIELD_GREEN, COLOR_FIELD_LINES, COLOR_BLUE, COLOR_GOLD,
    SECTION_COLORS, MARCHER_SIZE, FIELD_LENGTH, FIELD_WIDTH
)
from gameplay.band_api import BandMember



class FieldView:
    """Renders the marching field with Retro Bowl aesthetic."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
        # Font for labels (initialize before rendering)
        self.font_small = pygame.font.SysFont('arial', 10, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 14, bold=True)
        
        # Create surfaces for field
        self.field_surface = pygame.Surface((width, height))
        self._render_field()
        
        # Animation state
        self.show_grid = True
        self.show_coordinates = False
        self.show_section_labels = True
        
        # Grid settings
        self.grid_steps = 4  # 4 steps per 5 yards
        
    def _render_field(self):
        """Render the static football field background."""
        # Fill with grass green
        self.field_surface.fill(COLOR_FIELD_GREEN)
        
        # Draw border
        pygame.draw.rect(self.field_surface, COLOR_FIELD_LINES, 
                        (0, 0, self.width, self.height), 3)
        
        # Draw yard lines (every 5 yards)
        for yard in range(0, 101, 5):
            x = self._yard_to_pixel_x(yard)
            
            # Thicker lines for 10-yard marks
            thickness = 2 if yard % 10 == 0 else 1
            pygame.draw.line(self.field_surface, COLOR_FIELD_LINES,
                           (x, 5), (x, self.height - 5), thickness)
            
            # Draw yard numbers at major lines
            if yard % 10 == 0 and 0 < yard < 100:
                label = str(yard if yard <= 50 else 100 - yard)
                text = self.font_small.render(label, True, COLOR_FIELD_LINES)
                text_rect = text.get_rect(center=(x, 15))
                self.field_surface.blit(text, text_rect)
                
        # Draw hash marks (sideline to sideline)
        for hash_pos in [13.33, 26.67, 40.0]:  # Simplified hash positions
            y = self._yard_to_pixel_y(hash_pos)
            for yard in range(0, 101, 1):
                if yard % 5 != 0:  # Don't draw on yard lines
                    x = self._yard_to_pixel_x(yard)
                    pygame.draw.line(self.field_surface, COLOR_FIELD_LINES,
                                   (x, y - 2), (x, y + 2), 1)
                    
        # Draw 50-yard line in gold
        x_50 = self._yard_to_pixel_x(50)
        pygame.draw.line(self.field_surface, COLOR_GOLD,
                        (x_50, 5), (x_50, self.height - 5), 3)
        
        # Draw end zones
        pygame.draw.rect(self.field_surface, (100, 100, 100), 
                        (0, 0, self._yard_to_pixel_x(10), self.height))
        pygame.draw.rect(self.field_surface, (100, 100, 100), 
                        (self.width - self._yard_to_pixel_x(10), 0, self._yard_to_pixel_x(10), self.height))
        
    def _yard_to_pixel_x(self, yard: float) -> int:
        """Convert yard line (0-100) to pixel x coordinate."""
        return int((yard / FIELD_LENGTH) * (self.width - 10) + 5)
        
    def _yard_to_pixel_y(self, yard: float) -> int:
        """Convert yard position (0-53.33) to pixel y coordinate."""
        return int((yard / FIELD_WIDTH) * (self.height - 10) + 5)
        
    def _pixel_to_yard_x(self, pixel_x: int) -> float:
        """Convert pixel x to yard position."""
        return ((pixel_x - 5) / (self.width - 10)) * FIELD_LENGTH
        
    def _pixel_to_yard_y(self, pixel_y: int) -> float:
        """Convert pixel y to yard position."""
        return ((pixel_y - 5) / (self.height - 10)) * FIELD_WIDTH
        
    def _draw_marcher_sprite(self, surface: pygame.Surface, x: int, y: int, 
                            section: str, facing: float = 0, selected: bool = False):
        """Draw a Retro Bowl-style 8x8 pixel marcher sprite.
        
        Args:
            surface: Surface to draw on
            x, y: Center position in pixels
            section: Band section for color
            facing: Direction in degrees (0 = up)
            selected: Whether the marcher is selected
        """
        color = SECTION_COLORS.get(section, COLOR_GOLD)
        
        # Create 8x8 sprite
        sprite = pygame.Surface((MARCHER_SIZE, MARCHER_SIZE), pygame.SRCALPHA)
        
        # Draw simple character (head + body)
        # Head (top 3 pixels)
        pygame.draw.circle(sprite, (50, 40, 30), (4, 2), 2)
        
        # Body (colored uniform)
        pygame.draw.rect(sprite, color, (2, 4, 4, 4))
        
        # Add directional indicator (small dot showing facing)
        if facing == 0:  # Forward
            pygame.draw.circle(sprite, (255, 255, 255), (4, 1), 1)
        elif facing == 180:  # Backward
            pygame.draw.circle(sprite, (255, 255, 255), (4, 7), 1)
        elif facing == 90:  # Right
            pygame.draw.circle(sprite, (255, 255, 255), (7, 4), 1)
        elif facing == 270:  # Left
            pygame.draw.circle(sprite, (255, 255, 255), (1, 4), 1)
            
        # Add selection highlight
        if selected:
            pygame.draw.rect(sprite, (255, 255, 255), (0, 0, MARCHER_SIZE, MARCHER_SIZE), 1)
            
        # Blit sprite centered at position
        surface.blit(sprite, (x - MARCHER_SIZE // 2, y - MARCHER_SIZE // 2))
        
    def draw(self, surface: pygame.Surface, members: List[BandMember], selected_member: Optional[BandMember] = None):
        """Draw the field and all band members.
        
        Args:
            surface: Main game surface
            members: List of BandMember objects to render
            selected_member: Currently selected member (if any)
        """
        # Draw field background
        surface.blit(self.field_surface, (self.x, self.y))
        
        # Draw optional grid overlay
        if self.show_grid:
            self._draw_grid(surface)
            
        # Draw all band members
        for member in members:
            px = self.x + self._yard_to_pixel_x(member.x)
            py = self.y + self._yard_to_pixel_y(member.y)
            is_selected = selected_member is not None and selected_member.id == member.id
            self._draw_marcher_sprite(surface, px, py, member.section, member.facing, is_selected)
            
            # Show coordinates if enabled
            if self.show_coordinates:
                coord_text = f"({member.x:.0f},{member.y:.0f})"
                text_surf = self.font_small.render(coord_text, True, COLOR_FIELD_LINES)
                surface.blit(text_surf, (px - 15, py + 8))
                
            # Show section labels if enabled
            if self.show_section_labels:
                label_text = member.section[:1].upper()  # First letter of section
                text_surf = self.font_small.render(label_text, True, (255, 255, 255))
                surface.blit(text_surf, (px - 3, py - 12))
                
    def _draw_grid(self, surface: pygame.Surface):
        """Draw a subtle grid overlay for coding reference."""
        # Draw vertical lines every 5 yards
        for yard in range(0, 101, 5):
            x = self.x + self._yard_to_pixel_x(yard)
            pygame.draw.line(surface, (255, 255, 255, 40),
                           (x, self.y), (x, self.y + self.height), 1)
            
        # Draw horizontal lines every ~10 yards
        for yard in [0, 13.33, 26.67, 40.0, 53.33]:
            y = self.y + self._yard_to_pixel_y(yard)
            pygame.draw.line(surface, (255, 255, 255, 40),
                           (self.x, y), (self.x + self.width, y), 1)
                           
        # Draw finer grid steps (4 steps per 5 yards)
        step_yards = 5.0 / self.grid_steps
        for yard_x in [i * step_yards for i in range(int(100 / step_yards) + 1)]:
            x = self.x + self._yard_to_pixel_x(yard_x)
            pygame.draw.line(surface, (200, 200, 200, 20),
                           (x, self.y), (x, self.y + self.height), 1)
                           
        for yard_y in [i * step_yards for i in range(int(53.33 / step_yards) + 1)]:
            y = self.y + self._yard_to_pixel_y(yard_y)
            pygame.draw.line(surface, (200, 200, 200, 20),
                           (self.x, y), (self.x + self.width, y), 1)
                           
    def toggle_grid(self):
        """Toggle grid display."""
        self.show_grid = not self.show_grid
        
    def toggle_coordinates(self):
        """Toggle coordinate display."""
        self.show_coordinates = not self.show_coordinates
        
    def toggle_section_labels(self):
        """Toggle section label display."""
        self.show_section_labels = not self.show_section_labels
        
    def get_yard_at_mouse(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[float, float]]:
        """Convert mouse position to field coordinates.
        
        Returns:
            (x_yard, y_yard) or None if outside field
        """
        mx, my = mouse_pos
        if not self.rect.collidepoint(mx, my):
            return None
            
        rel_x = mx - self.x
        rel_y = my - self.y
        
        yard_x = self._pixel_to_yard_x(rel_x)
        yard_y = self._pixel_to_yard_y(rel_y)
        
        return (yard_x, yard_y)
        
    def get_member_at_mouse(self, mouse_pos: Tuple[int, int], members: List[BandMember]) -> Optional[BandMember]:
        """Get the band member at the mouse position.
        
        Args:
            mouse_pos: Mouse position (x, y)
            members: List of band members
            
        Returns:
            BandMember at position or None
        """
        mx, my = mouse_pos
        if not self.rect.collidepoint(mx, my):
            return None
            
        # Convert mouse to yard coordinates
        yard_pos = self.get_yard_at_mouse(mouse_pos)
        if not yard_pos:
            return None
            
        yard_x, yard_y = yard_pos
        
        # Find the closest member within a threshold
        threshold = 2.0  # yards
        closest_member = None
        closest_distance = float('inf')
        
        for member in members:
            distance = math.sqrt((member.x - yard_x)**2 + (member.y - yard_y)**2)
            if distance < threshold and distance < closest_distance:
                closest_member = member
                closest_distance = distance
                
        return closest_member
"""
Editor Scene - Main coding environment for Code of Pride.

This module provides the main coding environment with split-screen layout
for the code editor and field view.
"""

import pygame
from typing import List, Tuple, Optional
from ui.editor import CodeEditor
from ui.field_view import FieldView
from ui.timeline import Timeline
from gameplay.code_executor import CodeExecutor
from gameplay.scoring import PridePoints
from gameplay.band_api import BandMember
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, EDITOR_X, EDITOR_Y, 
    EDITOR_WIDTH, EDITOR_HEIGHT, FIELD_OFFSET_X, FIELD_OFFSET_Y,
    FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT, COLOR_BG, COLOR_BLUE, COLOR_GOLD
)


class EditorScene:
    """Main editor scene with split-screen layout."""
    
    def __init__(self):
        # Create UI components
        self.editor = CodeEditor(
            pygame.Rect(EDITOR_X, EDITOR_Y, EDITOR_WIDTH, EDITOR_HEIGHT)
        )
        
        self.field_view = FieldView(
            FIELD_OFFSET_X, FIELD_OFFSET_Y, 
            FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT
        )
        
        self.timeline = Timeline(
            20, WINDOW_HEIGHT - 100, 
            WINDOW_WIDTH - 40, 80
        )
        
        self.scorer = PridePoints()
        
        # Code executor
        self.executor = CodeExecutor()
        
        # State
        self.selected_member: Optional[BandMember] = None
        self.show_detailed_scores = False
        self.last_execute_time = 0
        
        # Font setup
        self.title_font = pygame.font.SysFont('arial', 24, bold=True)
        self.info_font = pygame.font.SysFont('arial', 14)
        
        # Colors
        self.colors = {
            'background': COLOR_BG,
            'panel_bg': (25, 25, 35),
            'border': (80, 80, 100),
            'text': (240, 240, 240),
            'highlight': COLOR_GOLD
        }
        
    def handle_event(self, event) -> str:
        """Handle pygame events.
        
        Returns:
            String indicating scene change or None
        """
        # Handle timeline events first
        if self.timeline.handle_event(event):
            return None
            
        # Handle editor events
        self.editor.handle_event(event)
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            mod = pygame.key.get_mods()
            ctrl = mod & pygame.KMOD_CTRL
            
            if ctrl and event.key == pygame.K_r:
                self.execute_code()
                return None
            elif ctrl and event.key == pygame.K_g:
                self.field_view.toggle_grid()
                return None
            elif ctrl and event.key == pygame.K_c:
                self.field_view.toggle_coordinates()
                return None
            elif ctrl and event.key == pygame.K_l:
                self.field_view.toggle_section_labels()
                return None
            elif ctrl and event.key == pygame.K_d:
                self.show_detailed_scores = not self.show_detailed_scores
                return None
                
        # Handle mouse events for field interaction
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if click is on field
                if self.field_view.rect.collidepoint(event.pos):
                    # Get member at mouse position
                    members = self.executor.get_band_members()
                    clicked_member = self.field_view.get_member_at_mouse(event.pos, members)
                    self.selected_member = clicked_member
                    return None
                    
        return None
        
    def update(self, dt: float):
        """Update scene state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update timeline
        self.timeline.update(dt)
        
        # Update band member animations
        members = self.executor.get_band_members()
        for member in members:
            # Update step phase for walking animation
            member.step_phase = (member.step_phase + dt * 2) % 1.0
            
    def execute_code(self):
        """Execute the code in the editor."""
        code = '\n'.join(self.editor.lines)
        success, output = self.executor.execute(code)
        
        if success:
            # Award points for successful execution
            points = self.scorer.add_points(25.0, "Correct formation")
            print(f"Awarded {points:.1f} points for correct formation")
        else:
            # Reset streak for errors
            self.scorer.reset_streak()
            print(f"Execution failed: {output}")
            
        self.last_execute_time = pygame.time.get_ticks()
        
    def draw(self, surface: pygame.Surface):
        """Draw the editor scene.
        
        Args:
            surface: Surface to draw on
        """
        # Draw background
        surface.fill(self.colors['background'])
        
        # Draw panels
        self._draw_panels(surface)
        
        # Draw UI components
        self.editor.draw(surface)
        members = self.executor.get_band_members()
        self.field_view.draw(surface, members, self.selected_member)
        self.timeline.draw(surface)
        self.scorer.draw(surface, 20, 20)
        
        # Draw detailed scores if requested
        if self.show_detailed_scores:
            self.scorer.draw_detailed(surface, WINDOW_WIDTH - 270, 20)
            
        # Draw titles
        self._draw_titles(surface)
        
        # Draw status bar
        self._draw_status_bar(surface)
        
    def _draw_panels(self, surface: pygame.Surface):
        """Draw the background panels for the split-screen layout."""
        # Editor panel
        editor_rect = pygame.Rect(
            EDITOR_X - 10, EDITOR_Y - 30,
            EDITOR_WIDTH + 20, EDITOR_HEIGHT + 40
        )
        pygame.draw.rect(surface, self.colors['panel_bg'], editor_rect)
        pygame.draw.rect(surface, self.colors['border'], editor_rect, 2)
        
        # Field panel
        field_rect = pygame.Rect(
            FIELD_OFFSET_X - 10, FIELD_OFFSET_Y - 30,
            FIELD_PIXEL_WIDTH + 20, FIELD_PIXEL_HEIGHT + 40
        )
        pygame.draw.rect(surface, self.colors['panel_bg'], field_rect)
        pygame.draw.rect(surface, self.colors['border'], field_rect, 2)
        
        # Timeline panel
        timeline_rect = pygame.Rect(
            10, WINDOW_HEIGHT - 110,
            WINDOW_WIDTH - 20, 90
        )
        pygame.draw.rect(surface, self.colors['panel_bg'], timeline_rect)
        pygame.draw.rect(surface, self.colors['border'], timeline_rect, 2)
        
    def _draw_titles(self, surface: pygame.Surface):
        """Draw panel titles."""
        # Editor title
        editor_title = self.title_font.render("Python Code Editor", True, self.colors['highlight'])
        surface.blit(editor_title, (EDITOR_X, EDITOR_Y - 25))
        
        # Field title
        field_title = self.title_font.render("Marching Field Simulator", True, self.colors['highlight'])
        surface.blit(field_title, (FIELD_OFFSET_X, FIELD_OFFSET_Y - 25))
        
    def _draw_status_bar(self, surface: pygame.Surface):
        """Draw the status bar with helpful information."""
        # Status bar background
        status_rect = pygame.Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20)
        pygame.draw.rect(surface, (30, 30, 40), status_rect)
        pygame.draw.line(surface, self.colors['border'], 
                        (0, WINDOW_HEIGHT - 20), (WINDOW_WIDTH, WINDOW_HEIGHT - 20), 1)
        
        # Status text
        status_text = "Ctrl+R: Run Code | Ctrl+G: Toggle Grid | Ctrl+C: Toggle Coordinates | Ctrl+L: Toggle Labels | Ctrl+D: Toggle Score Details"
        text = self.info_font.render(status_text, True, (200, 200, 200))
        surface.blit(text, (10, WINDOW_HEIGHT - 17))
        
    def resize(self, width: int, height: int):
        """Handle window resize.
        
        Args:
            width: New window width
            height: New window height
        """
        # Resize timeline
        self.timeline.rect.width = width - 40
        self.timeline.width = width - 40
        
        # Update status bar position
        # (It's automatically positioned at the bottom)
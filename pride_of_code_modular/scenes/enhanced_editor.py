"""Enhanced Editor Scene - Main gameplay view with split-screen layout.

Left: Code editor with Python console
Right: Field view with marching band visualization
Bottom: Controls and output
"""

import pygame
from core.state_manager import State
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_BLUE, COLOR_GOLD, COLOR_TEXT,
    EDITOR_X, EDITOR_Y, EDITOR_WIDTH, EDITOR_HEIGHT,
    FIELD_OFFSET_X, FIELD_OFFSET_Y, FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT
)
from ui.field_view import FieldView
from gameplay.code_executor import CodeExecutor


class EnhancedEditorScene(State):
    """Main gameplay scene with code editor and field view."""
    
    def __init__(self, manager, game, level_manager):
        self.manager = manager
        self.game = game
        self.level_manager = level_manager
        
        # Fonts
        self.font_title = pygame.font.SysFont('arial', 24, bold=True)
        self.font_normal = pygame.font.SysFont('arial', 16)
        self.font_small = pygame.font.SysFont('arial', 14)
        
        # Field view
        self.field_view = FieldView(
            FIELD_OFFSET_X, FIELD_OFFSET_Y,
            FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT
        )
        
        # Code executor
        self.executor = CodeExecutor()
        
        # State
        self.level_id = None
        self.level_data = None
        self.output_text = "Ready to code! Press Ctrl+R to run your program."
        self.is_running = False
        self.show_help = False
        
        # Initial sample code
        self.initial_code = [
            "# Pride of Code - Week 1: Variables & Movement",
            "# The 'band' object controls the marching band",
            "",
            "# Get the first band member",
            "member = members[0]",
            "",
            "# Move them to position (50, 25) on the field",
            "band.move_to(member, 50, 25)",
            "",
            "# Print their position",
            "print(f'Member at ({member.x}, {member.y})')"
        ]
        
    def enter(self, **params):
        """Initialize the scene when entered."""
        self.level_id = params.get('level_id', 'week1')
        self.level_data = self.level_manager.get_level(self.level_id) if self.level_id else None
        
        # Reset editor with initial code
        if hasattr(self.game, 'editor'):
            self.game.editor.lines = list(self.initial_code)
            self.game.editor.cursor = [0, 0]
            self.game.editor.scroll = 0
            
        # Initialize band
        self.executor.reset()
        self.executor.band_api.create_band(16)
        self.output_text = "Ready to code! Press Ctrl+R to run your program."
        
    def handle_event(self, ev):
        """Handle input events."""
        if ev.type == pygame.KEYDOWN:
            # ESC to return to menu
            if ev.key == pygame.K_ESCAPE:
                self.manager.switch('menu')
                
            # Ctrl+R to run code
            elif ev.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.run_code()
                
            # Ctrl+H to toggle help
            elif ev.key == pygame.K_h and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.show_help = not self.show_help
                
            # F1 to reset band
            elif ev.key == pygame.K_F1:
                self.executor.reset()
                self.executor.band_api.create_band(16)
                self.output_text = "Band reset to starting formation."
                
            # F2 to toggle grid
            elif ev.key == pygame.K_F2:
                self.field_view.toggle_grid()
                
            # F3 to toggle coordinates
            elif ev.key == pygame.K_F3:
                self.field_view.toggle_coordinates()
                
    def run_code(self):
        """Execute the code from the editor."""
        if not hasattr(self.game, 'editor'):
            return
            
        code = '\n'.join(self.game.editor.lines)
        
        # Check for syntax errors first
        ok, msg = self.game.editor.check_syntax()
        if not ok:
            self.output_text = f"❌ {msg}"
            return
            
        # Execute code
        self.is_running = True
        success, output = self.executor.execute(code, initial_band_size=16)
        
        if success:
            self.output_text = f"✓ Code executed successfully!\n\n{output}"
        else:
            self.output_text = f"❌ Error:\n{output}"
            
        self.is_running = False
        
    def update(self, dt):
        """Update scene state."""
        pass
        
    def draw(self, surface):
        """Render the scene."""
        # Background
        surface.fill(COLOR_BG)
        
        # === LEFT SIDE: CODE EDITOR ===
        
        # Title bar
        title_text = self.font_title.render('Pride of Code', True, COLOR_GOLD)
        surface.blit(title_text, (20, 20))
        
        level_text = self.font_normal.render(
            f'Level: {self.level_id or "Sandbox"}', True, COLOR_TEXT
        )
        surface.blit(level_text, (20, 55))
        
        # Controls hint
        hint_text = self.font_small.render(
            'Ctrl+R: Run | Ctrl+H: Help | F1: Reset | ESC: Menu',
            True, (150, 150, 150)
        )
        surface.blit(hint_text, (20, 85))
        
        # Editor
        if hasattr(self.game, 'editor'):
            self.game.editor.rect = pygame.Rect(EDITOR_X, EDITOR_Y, EDITOR_WIDTH, EDITOR_HEIGHT)
            self.game.editor.draw(surface)
            
        # === RIGHT SIDE: FIELD VIEW ===
        
        # Field title
        field_title = self.font_title.render('Marching Field', True, COLOR_GOLD)
        title_rect = field_title.get_rect(centerx=FIELD_OFFSET_X + FIELD_PIXEL_WIDTH // 2, y=20)
        surface.blit(field_title, title_rect)
        
        # Field view
        members = self.executor.get_band_members()
        self.field_view.draw(surface, members)
        
        # Band member count
        count_text = self.font_small.render(
            f'Band Members: {len(members)}', True, COLOR_TEXT
        )
        surface.blit(count_text, (FIELD_OFFSET_X, FIELD_OFFSET_Y + FIELD_PIXEL_HEIGHT + 10))
        
        # === BOTTOM: OUTPUT CONSOLE ===
        
        output_y = EDITOR_Y + EDITOR_HEIGHT + 10
        output_rect = pygame.Rect(20, output_y, WINDOW_WIDTH - 40, 40)
        pygame.draw.rect(surface, (30, 30, 40), output_rect)
        pygame.draw.rect(surface, COLOR_BLUE, output_rect, 2)
        
        # Output text (truncated to fit)
        output_lines = self.output_text.split('\n')
        y_offset = output_y + 5
        for i, line in enumerate(output_lines[:2]):  # Show first 2 lines
            text_surf = self.font_small.render(line[:100], True, COLOR_TEXT)
            surface.blit(text_surf, (25, y_offset))
            y_offset += 18
            
        # === HELP OVERLAY ===
        
        if self.show_help:
            self._draw_help_overlay(surface)
            
    def _draw_help_overlay(self, surface):
        """Draw help overlay with API reference."""
        # Semi-transparent background
        overlay = pygame.Surface((600, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (WINDOW_WIDTH // 2 - 300, 100))
        
        # Help text
        help_lines = [
            "BAND API REFERENCE",
            "",
            "Variables Available:",
            "  band        - Band controller object",
            "  members     - List of all band members",
            "  brass       - List of brass section members",
            "  woodwind    - List of woodwind members",
            "  percussion  - List of percussion members",
            "  guard       - List of color guard members",
            "",
            "Commands:",
            "  band.move_to(member, x, y)",
            "    Move a member to position (x, y)",
            "",
            "  band.move_forward(member, steps)",
            "    Move member forward by steps",
            "",
            "  band.form_circle(members, cx, cy, radius)",
            "    Arrange members in a circle",
            "",
            "  band.form_line(members, x1, y1, x2, y2)",
            "    Arrange members in a line",
            "",
            "Press Ctrl+H to close"
        ]
        
        y = 120
        for i, line in enumerate(help_lines):
            if i == 0:  # Title
                text = self.font_title.render(line, True, COLOR_GOLD)
            else:
                text = self.font_small.render(line, True, COLOR_TEXT)
            text_rect = text.get_rect(centerx=WINDOW_WIDTH // 2, y=y)
            surface.blit(text, text_rect)
            y += 22 if i == 0 else 20
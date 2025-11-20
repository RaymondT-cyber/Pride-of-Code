"""
Sandbox Mode - Freeform practice for Code of Pride.

This module implements the sandbox mode where players can experiment
without any specific goals or constraints.
"""

import pygame
import random
from typing import List, Dict, Optional
from gameplay.band_api import BandAPI
from gameplay.scoring import PridePoints


class SandboxMode:
    """Manages the freeform sandbox mode."""
    
    def __init__(self):
        self.band_api = BandAPI()
        self.scorer = PridePoints()
        
        # Sandbox settings
        self.band_size = 16
        self.grid_visible = True
        self.coordinates_visible = False
        self.section_labels_visible = True
        
        # Custom formations
        self.saved_formations = []
        self.current_formation = None
        
        # Tools
        self.selected_tool = 'select'  # 'select', 'move', 'paint'
        self.paint_brush_size = 3
        self.paint_section = 'brass'
        
        # Animation
        self.animation_speed = 1.0
        self.animation_playing = False
        
        # Initialize band
        self.band_api.create_band(self.band_size)
        
    def set_band_size(self, size: int):
        """Set the number of band members.
        
        Args:
            size: Number of band members
        """
        self.band_size = max(1, min(50, size))  # Limit between 1 and 50
        self.band_api.create_band(self.band_size)
        
    def get_band_members(self):
        """Get all band members.
        
        Returns:
            List of band members
        """
        return self.band_api.get_all_members()
        
    def execute_code(self, code: str) -> Dict:
        """Execute code in the sandbox environment.
        
        Args:
            code: Code to execute
            
        Returns:
            Dictionary with execution results
        """
        # In a real implementation, we would execute the code
        # For now, we'll just simulate success
        try:
            # This would be the actual code execution
            # exec(code, {'band': self.band_api})
            success = True
            message = "Code executed successfully"
        except Exception as e:
            success = False
            message = f"Error: {str(e)}"
            
        return {
            'success': success,
            'message': message
        }
        
    def save_formation(self, name: str) -> bool:
        """Save the current formation.
        
        Args:
            name: Name for the formation
            
        Returns:
            True if saved successfully, False otherwise
        """
        members = self.band_api.get_all_members()
        if not members:
            return False
            
        # Save member positions
        formation = {
            'name': name,
            'members': [
                {
                    'id': m.id,
                    'x': m.x,
                    'y': m.y,
                    'section': m.section,
                    'instrument': m.instrument
                }
                for m in members
            ]
        }
        
        self.saved_formations.append(formation)
        self.current_formation = formation
        
        return True
        
    def load_formation(self, index: int) -> bool:
        """Load a saved formation.
        
        Args:
            index: Index of formation to load
            
        Returns:
            True if loaded successfully, False otherwise
        """
        if index < 0 or index >= len(self.saved_formations):
            return False
            
        formation = self.saved_formations[index]
        self.current_formation = formation
        
        # Apply formation to band members
        members = self.band_api.get_all_members()
        for saved_member in formation['members']:
            if saved_member['id'] < len(members):
                member = members[saved_member['id']]
                member.x = saved_member['x']
                member.y = saved_member['y']
                member.section = saved_member['section']
                member.instrument = saved_member['instrument']
                
        return True
        
    def get_saved_formations(self) -> List[Dict]:
        """Get list of saved formations.
        
        Returns:
            List of saved formations
        """
        return self.saved_formations.copy()
        
    def delete_formation(self, index: int) -> bool:
        """Delete a saved formation.
        
        Args:
            index: Index of formation to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if index < 0 or index >= len(self.saved_formations):
            return False
            
        del self.saved_formations[index]
        
        # Update current formation if needed
        if self.current_formation and index < len(self.saved_formations):
            self.current_formation = self.saved_formations[index] if self.saved_formations else None
            
        return True
        
    def clear_band(self):
        """Clear all band members to starting positions."""
        self.band_api.create_band(self.band_size)
        
    def randomize_band(self):
        """Randomize band member positions."""
        members = self.band_api.get_all_members()
        for member in members:
            member.x = random.uniform(10, 90)
            member.y = random.uniform(10, 45)
            
    def toggle_grid(self):
        """Toggle grid visibility."""
        self.grid_visible = not self.grid_visible
        
    def toggle_coordinates(self):
        """Toggle coordinate visibility."""
        self.coordinates_visible = not self.coordinates_visible
        
    def toggle_section_labels(self):
        """Toggle section label visibility."""
        self.section_labels_visible = not self.section_labels_visible
        
    def set_tool(self, tool: str):
        """Set the current tool.
        
        Args:
            tool: Tool to select ('select', 'move', 'paint')
        """
        if tool in ['select', 'move', 'paint']:
            self.selected_tool = tool
            
    def set_paint_brush_size(self, size: int):
        """Set the paint brush size.
        
        Args:
            size: Brush size
        """
        self.paint_brush_size = max(1, min(10, size))
        
    def set_paint_section(self, section: str):
        """Set the paint section.
        
        Args:
            section: Section to paint ('brass', 'woodwind', 'percussion', 'guard')
        """
        if section in ['brass', 'woodwind', 'percussion', 'guard']:
            self.paint_section = section
            
    def handle_mouse_click(self, x: float, y: float):
        """Handle mouse click in the field view.
        
        Args:
            x: X coordinate in yards
            y: Y coordinate in yards
        """
        if self.selected_tool == 'move':
            # Move selected member to position
            # This would require a selected member to be tracked
            pass
        elif self.selected_tool == 'paint':
            # Paint members in area
            self._paint_area(x, y)
            
    def _paint_area(self, center_x: float, center_y: float):
        """Paint band members in an area.
        
        Args:
            center_x: Center X coordinate
            center_y: Center Y coordinate
        """
        members = self.band_api.get_all_members()
        brush_radius = self.paint_brush_size * 1.5
        
        for member in members:
            distance = ((member.x - center_x) ** 2 + (member.y - center_y) ** 2) ** 0.5
            if distance <= brush_radius:
                member.section = self.paint_section
                
    def set_animation_speed(self, speed: float):
        """Set animation speed.
        
        Args:
            speed: Animation speed multiplier
        """
        self.animation_speed = max(0.1, min(5.0, speed))
        
    def toggle_animation(self):
        """Toggle animation playback."""
        self.animation_playing = not self.animation_playing
        
    def update(self, dt: float):
        """Update sandbox state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.animation_playing:
            # Update animations
            members = self.band_api.get_all_members()
            for member in members:
                # Update step phase for walking animation
                member.step_phase = (member.step_phase + dt * 2 * self.animation_speed) % 1.0
                
    def get_sandbox_state(self) -> Dict:
        """Get the current sandbox state.
        
        Returns:
            Dictionary with sandbox state information
        """
        return {
            'band_size': self.band_size,
            'grid_visible': self.grid_visible,
            'coordinates_visible': self.coordinates_visible,
            'section_labels_visible': self.section_labels_visible,
            'selected_tool': self.selected_tool,
            'paint_brush_size': self.paint_brush_size,
            'paint_section': self.paint_section,
            'animation_speed': self.animation_speed,
            'animation_playing': self.animation_playing,
            'saved_formations_count': len(self.saved_formations)
        }
        
    def reset_sandbox(self):
        """Reset the sandbox to initial state."""
        self.band_size = 16
        self.grid_visible = True
        self.coordinates_visible = False
        self.section_labels_visible = True
        self.selected_tool = 'select'
        self.paint_brush_size = 3
        self.paint_section = 'brass'
        self.animation_speed = 1.0
        self.animation_playing = False
        self.saved_formations.clear()
        self.current_formation = None
        self.band_api.create_band(self.band_size)


# We need to import random for the randomize_band method
import random
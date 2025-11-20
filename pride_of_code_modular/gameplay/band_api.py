"""
Band API - Pre-defined commands for controlling the marching band.

This module provides a simple, Pythonic API that students can use
to control band members on the field.
"""

import math
from typing import List, Tuple, Dict, Any, Optional


class BandMember:
    """Represents a single band member with position and properties."""
    
    def __init__(self, id: int, x: float, y: float, section: str = 'brass', instrument: str = 'trumpet'):
        self.id = id
        self.x = x  # Position in yards from left sideline
        self.y = y  # Position in yards from back sideline
        self.section = section
        self.instrument = instrument
        self.facing = 0  # Direction in degrees (0 = up field)
        
        # Animation properties
        self.step_phase = 0  # For walking animation
        self.selected = False  # Is this member selected?
        
    def __repr__(self):
        return f"BandMember({self.id}, x={self.x:.1f}, y={self.y:.1f}, {self.section})"


class BandAPI:
    """Main API for controlling the marching band.
    
    This class provides methods that students can call from their Python code
    to move and manipulate band members.
    """
    
    def __init__(self):
        self.members: List[BandMember] = []
        self.animation_queue: List[Dict[str, Any]] = []
        self.sections: Dict[str, List[BandMember]] = {
            'brass': [],
            'woodwind': [],
            'percussion': [],
            'guard': []
        }
        
    def reset(self):
        """Clear all members and animations."""
        self.members = []
        self.animation_queue = []
        for section in self.sections.values():
            section.clear()
            
    def create_band(self, size: int = 16):
        """Create a default band formation.
        
        Args:
            size: Number of band members to create
        """
        self.reset()
        
        # Create members in a simple block formation
        sections = ['brass', 'brass', 'brass', 'brass', 
                   'woodwind', 'woodwind', 'woodwind', 'woodwind',
                   'percussion', 'percussion', 'percussion', 'percussion',
                   'guard', 'guard', 'guard', 'guard']
        
        # Instruments for each section
        instruments = {
            'brass': ['trumpet', 'trombone', 'french horn', 'tuba'],
            'woodwind': ['flute', 'clarinet', 'saxophone', 'oboe'],
            'percussion': ['snare', 'bass drum', 'cymbals', 'mallets'],
            'guard': ['flag', 'rifle', 'saber', 'banner']
        }
        
        rows = 4
        cols = size // rows
        start_x = 20  # Start at 20-yard line
        start_y = 15  # 15 yards from back sideline
        
        for i in range(size):
            row = i // cols
            col = i % cols
            x = start_x + col * 5
            y = start_y + row * 8
            section = sections[i % len(sections)]
            
            # Select instrument based on position in section
            instr_list = instruments[section]
            instrument = instr_list[i % len(instr_list)]
            
            member = BandMember(i, x, y, section, instrument)
            self.members.append(member)
            self.sections[section].append(member)
            
    def get_member(self, id: int) -> Optional[BandMember]:
        """Get a band member by ID."""
        for member in self.members:
            if member.id == id:
                return member
        return None
        
    def get_section(self, section: str) -> List[BandMember]:
        """Get all members of a specific section."""
        return self.sections.get(section, [])
        
    # ============== STUDENT-FACING API METHODS ==============
    
    def move_to(self, member, x: float, y: float):
        """Move a band member to a specific position.
        
        Args:
            member: BandMember object or member ID
            x: X coordinate in yards (0-100)
            y: Y coordinate in yards (0-53.33)
        """
        if isinstance(member, int):
            member = self.get_member(member)
        if member:
            member.x = max(0, min(x, 100))
            member.y = max(0, min(y, 53.33))
            self.animation_queue.append({
                'type': 'move',
                'member': member,
                'target': (member.x, member.y)
            })
            
    def move_forward(self, member, steps: int):
        """Move a band member forward by a number of steps.
        
        Args:
            member: BandMember object or member ID
            steps: Number of steps to move (negative = backward)
        """
        if isinstance(member, int):
            member = self.get_member(member)
        if member:
            # Calculate new position based on facing direction
            radians = math.radians(member.facing)
            dx = math.sin(radians) * steps * 0.8  # 0.8 yards per step
            dy = math.cos(radians) * steps * 0.8
            self.move_to(member, member.x + dx, member.y + dy)
            
    def turn(self, member, direction: str):
        """Turn a band member to face a direction.
        
        Args:
            member: BandMember object or member ID
            direction: 'left', 'right', 'forward', 'backward', or angle in degrees
        """
        if isinstance(member, int):
            member = self.get_member(member)
        if member:
            if direction == 'left':
                member.facing = 270
            elif direction == 'right':
                member.facing = 90
            elif direction == 'forward':
                member.facing = 0
            elif direction == 'backward':
                member.facing = 180
            elif isinstance(direction, (int, float)):
                member.facing = direction % 360
                
    def form_line(self, members: List, start_x: float, start_y: float, 
                  end_x: float, end_y: float):
        """Arrange members in a straight line between two points.
        
        Args:
            members: List of BandMember objects or IDs
            start_x, start_y: Starting coordinate
            end_x, end_y: Ending coordinate
        """
        if not members:
            return
            
        count = len(members)
        for i, m in enumerate(members):
            if isinstance(m, int):
                m = self.get_member(m)
            if m:
                t = i / max(1, count - 1) if count > 1 else 0
                x = start_x + (end_x - start_x) * t
                y = start_y + (end_y - start_y) * t
                self.move_to(m, x, y)
                
    def form_circle(self, members: List, center_x: float, center_y: float, 
                    radius: float):
        """Arrange members in a circle.
        
        Args:
            members: List of BandMember objects or IDs
            center_x, center_y: Center of the circle
            radius: Radius in yards
        """
        if not members:
            return
            
        count = len(members)
        for i, m in enumerate(members):
            if isinstance(m, int):
                m = self.get_member(m)
            if m:
                angle = (2 * math.pi * i) / count
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.move_to(m, x, y)
                
    def form_block(self, members: List, x: float, y: float, 
                   rows: int, spacing: float = 5.0):
        """Arrange members in a rectangular block.
        
        Args:
            members: List of BandMember objects or IDs
            x, y: Top-left corner position
            rows: Number of rows
            spacing: Space between members in yards
        """
        if not members or rows <= 0:
            return
            
        cols = len(members) // rows
        if len(members) % rows != 0:
            cols += 1
            
        for i, m in enumerate(members):
            if isinstance(m, int):
                m = self.get_member(m)
            if m:
                row = i // cols
                col = i % cols
                new_x = x + col * spacing
                new_y = y + row * spacing
                self.move_to(m, new_x, new_y)
                
    def get_all_members(self) -> List[BandMember]:
        """Return all band members."""
        return self.members
        
    def print_positions(self):
        """Print current positions of all members (for debugging)."""
        for member in self.members:
            print(f"Member {member.id}: ({member.x:.1f}, {member.y:.1f}) - {member.section}")
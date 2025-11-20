"""
Timeline - Music & Tempo Timeline for Code of Pride.

This module provides a visual timeline that represents the musical beats 
and measures of the show's soundtrack, allowing players to synchronize 
movements to the music.
"""

import pygame
from typing import List, Tuple, Optional
from config import COLOR_BLUE, COLOR_GOLD, COLOR_BG, COLOR_TEXT


class Timeline:
    """A visual timeline for synchronizing movements to music."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
        # Timeline settings
        self.total_beats = 128  # Total beats in the timeline
        self.current_beat = 0   # Current position in the timeline
        self.beat_width = self.width / self.total_beats  # Width per beat in pixels
        self.playing = False    # Is the timeline currently playing?
        self.tempo = 120        # Tempo in BPM
        self.last_update = 0    # Last update time for timing
        
        # Font for labels
        self.font_small = pygame.font.SysFont('arial', 10)
        self.font_medium = pygame.font.SysFont('arial', 14)
        
        # Colors
        self.colors = {
            'background': (40, 40, 50),
            'beat_marker': (100, 100, 120),
            'measure_marker': (150, 150, 170),
            'current_beat': COLOR_GOLD,
            'playhead': COLOR_BLUE,
            'text': COLOR_TEXT
        }
        
    def update(self, dt: float):
        """Update the timeline position if playing.
        
        Args:
            dt: Delta time in seconds
        """
        if self.playing:
            # Calculate beats per second
            beats_per_second = self.tempo / 60.0
            # Update current beat based on time
            self.current_beat += beats_per_second * dt
            # Loop back to start if we've reached the end
            if self.current_beat >= self.total_beats:
                self.current_beat = 0
                
    def play(self):
        """Start playing the timeline."""
        self.playing = True
        self.last_update = pygame.time.get_ticks() / 1000.0
        
    def pause(self):
        """Pause the timeline."""
        self.playing = False
        
    def stop(self):
        """Stop and reset the timeline."""
        self.playing = False
        self.current_beat = 0
        
    def set_position(self, beat: float):
        """Set the current position in the timeline.
        
        Args:
            beat: Beat position (0 to total_beats)
        """
        self.current_beat = max(0, min(beat, self.total_beats - 1))
        
    def set_tempo(self, bpm: int):
        """Set the tempo of the timeline.
        
        Args:
            bpm: Beats per minute
        """
        self.tempo = max(30, min(bpm, 300))  # Constrain to reasonable range
        
    def draw(self, surface: pygame.Surface):
        """Draw the timeline.
        
        Args:
            surface: Surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, self.colors['background'], self.rect)
        pygame.draw.rect(surface, (80, 80, 100), self.rect, 2)
        
        # Draw beat markers
        for i in range(self.total_beats):
            x = self.x + i * self.beat_width
            # Draw measure markers (every 4 beats) taller
            if i % 4 == 0:
                pygame.draw.line(surface, self.colors['measure_marker'],
                               (x, self.y + self.height - 20), (x, self.y + self.height), 2)
                # Draw measure number
                measure_num = i // 4 + 1
                text = self.font_small.render(str(measure_num), True, self.colors['text'])
                surface.blit(text, (x + 2, self.y + 2))
            else:
                pygame.draw.line(surface, self.colors['beat_marker'],
                               (x, self.y + self.height - 10), (x, self.y + self.height), 1)
        
        # Draw current beat marker
        current_x = self.x + self.current_beat * self.beat_width
        pygame.draw.line(surface, self.colors['current_beat'],
                       (current_x, self.y), (current_x, self.y + self.height), 2)
        
        # Draw playhead
        playhead_y = self.y + self.height // 2
        pygame.draw.polygon(surface, self.colors['playhead'], [
            (current_x, playhead_y - 8),
            (current_x + 10, playhead_y),
            (current_x, playhead_y + 8)
        ])
        
        # Draw tempo info
        tempo_text = f"Tempo: {self.tempo} BPM"
        text = self.font_medium.render(tempo_text, True, self.colors['text'])
        surface.blit(text, (self.x + 10, self.y + 10))
        
        # Draw play/pause status
        status_text = "Playing" if self.playing else "Paused"
        status_color = self.colors['current_beat'] if self.playing else (150, 150, 150)
        text = self.font_medium.render(status_text, True, status_color)
        surface.blit(text, (self.x + self.width - 100, self.y + 10))
        
    def handle_event(self, event):
        """Handle mouse events for timeline interaction.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Calculate beat position from mouse click
                rel_x = event.pos[0] - self.x
                beat = rel_x / self.beat_width
                self.set_position(beat)
                return True
        return False
        
    def get_current_beat(self) -> float:
        """Get the current beat position.
        
        Returns:
            Current beat (0 to total_beats)
        """
        return self.current_beat
        
    def get_current_measure(self) -> int:
        """Get the current measure number.
        
        Returns:
            Current measure (1-indexed)
        """
        return int(self.current_beat // 4) + 1
        
    def is_on_downbeat(self) -> bool:
        """Check if we're currently on a downbeat (first beat of measure).
        
        Returns:
            True if on downbeat, False otherwise
        """
        return abs(self.current_beat % 4) < 0.1
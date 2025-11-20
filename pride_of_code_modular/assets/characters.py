"""
Character Sprites - Pixel art characters for Code of Pride.

This module defines the pixel art sprites for key characters in the game.
"""

import pygame
from typing import Dict, Tuple


class CharacterSprites:
    """Manages character sprites for the game."""
    
    def __init__(self):
        self.sprites = {}
        self._create_character_sprites()
        
    def _create_character_sprites(self):
        """Create pixel art sprites for key characters."""
        # Create simple 16x16 pixel sprites
        self.sprites['drum_major'] = self._create_drum_major_sprite()
        self.sprites['band_director'] = self._create_band_director_sprite()
        self.sprites['brass_leader'] = self._create_brass_leader_sprite()
        self.sprites['woodwind_leader'] = self._create_woodwind_leader_sprite()
        self.sprites['percussion_leader'] = self._create_percussion_leader_sprite()
        self.sprites['guard_leader'] = self._create_guard_leader_sprite()
        self.sprites['player'] = self._create_player_sprite()
        
    def _create_drum_major_sprite(self) -> pygame.Surface:
        """Create a sprite for the Drum Major."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (blue uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (blue uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (46, 94, 170), (11, 5, 2, 4))  # Right arm
        
        # Legs (blue uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (46, 94, 170), (8, 12, 2, 4))  # Right leg
        
        # Baton (white)
        pygame.draw.rect(sprite, (255, 255, 255), (12, 2, 1, 6))
        pygame.draw.circle(sprite, (255, 255, 255), (12, 2), 2)
        
        # Gold braid details
        pygame.draw.rect(sprite, (255, 184, 28), (5, 4, 6, 2))  # Shoulder braid
        
        return sprite
        
    def _create_band_director_sprite(self) -> pygame.Surface:
        """Create a sprite for the Band Director."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (black suit)
        pygame.draw.rect(sprite, (40, 40, 40), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (black suit)
        pygame.draw.rect(sprite, (40, 40, 40), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (40, 40, 40), (11, 5, 2, 4))  # Right arm
        
        # Legs (black suit)
        pygame.draw.rect(sprite, (40, 40, 40), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (40, 40, 40), (8, 12, 2, 4))  # Right leg
        
        # White shirt details
        pygame.draw.rect(sprite, (255, 255, 255), (6, 5, 4, 3))  # Shirt front
        pygame.draw.rect(sprite, (255, 255, 255), (5, 7, 1, 2))  # Left cuff
        pygame.draw.rect(sprite, (255, 255, 255), (10, 7, 1, 2))  # Right cuff
        
        # Conducting baton
        pygame.draw.rect(sprite, (200, 200, 200), (12, 3, 1, 7))
        
        return sprite
        
    def _create_brass_leader_sprite(self) -> pygame.Surface:
        """Create a sprite for the Brass Section Leader."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (gold uniform)
        pygame.draw.rect(sprite, (255, 215, 0), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (gold uniform)
        pygame.draw.rect(sprite, (255, 215, 0), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (255, 215, 0), (11, 5, 2, 4))  # Right arm
        
        # Legs (gold uniform)
        pygame.draw.rect(sprite, (255, 215, 0), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (255, 215, 0), (8, 12, 2, 4))  # Right leg
        
        # Trumpet
        pygame.draw.rect(sprite, (200, 200, 200), (12, 6, 2, 1))  # Mouthpiece
        pygame.draw.rect(sprite, (200, 200, 200), (14, 5, 1, 3))  # Bell
        
        # Section leader armband
        pygame.draw.rect(sprite, (255, 0, 0), (3, 5, 2, 1))  # Red armband
        
        return sprite
        
    def _create_woodwind_leader_sprite(self) -> pygame.Surface:
        """Create a sprite for the Woodwind Section Leader."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (light green uniform)
        pygame.draw.rect(sprite, (144, 238, 144), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (light green uniform)
        pygame.draw.rect(sprite, (144, 238, 144), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (144, 238, 144), (11, 5, 2, 4))  # Right arm
        
        # Legs (light green uniform)
        pygame.draw.rect(sprite, (144, 238, 144), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (144, 238, 144), (8, 12, 2, 4))  # Right leg
        
        # Clarinet
        pygame.draw.rect(sprite, (139, 69, 19), (12, 5, 1, 4))  # Body
        pygame.draw.rect(sprite, (139, 69, 19), (13, 6, 2, 1))  # Mouthpiece
        
        # Section leader armband
        pygame.draw.rect(sprite, (255, 0, 0), (3, 5, 2, 1))  # Red armband
        
        return sprite
        
    def _create_percussion_leader_sprite(self) -> pygame.Surface:
        """Create a sprite for the Percussion Section Leader."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (red uniform)
        pygame.draw.rect(sprite, (220, 20, 60), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (red uniform)
        pygame.draw.rect(sprite, (220, 20, 60), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (220, 20, 60), (11, 5, 2, 4))  # Right arm
        
        # Legs (red uniform)
        pygame.draw.rect(sprite, (220, 20, 60), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (220, 20, 60), (8, 12, 2, 4))  # Right leg
        
        # Drum sticks
        pygame.draw.rect(sprite, (139, 69, 19), (12, 5, 1, 3))  # Right stick
        pygame.draw.rect(sprite, (139, 69, 19), (2, 5, 1, 3))   # Left stick
        
        # Section leader armband
        pygame.draw.rect(sprite, (255, 0, 0), (3, 5, 2, 1))  # Red armband
        
        return sprite
        
    def _create_guard_leader_sprite(self) -> pygame.Surface:
        """Create a sprite for the Color Guard Leader."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (purple uniform)
        pygame.draw.rect(sprite, (186, 85, 211), (5, 4, 6, 8))  # Torso
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (purple uniform)
        pygame.draw.rect(sprite, (186, 85, 211), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (186, 85, 211), (11, 5, 2, 4))  # Right arm
        
        # Legs (purple uniform)
        pygame.draw.rect(sprite, (186, 85, 211), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (186, 85, 211), (8, 12, 2, 4))  # Right leg
        
        # Flag
        pygame.draw.rect(sprite, (255, 255, 255), (12, 3, 3, 5))  # Flag pole
        pygame.draw.rect(sprite, (255, 0, 0), (13, 3, 2, 2))     # Red part
        pygame.draw.rect(sprite, (0, 0, 255), (13, 5, 2, 2))     # Blue part
        
        # Section leader armband
        pygame.draw.rect(sprite, (255, 0, 0), (3, 5, 2, 1))  # Red armband
        
        return sprite
        
    def _create_player_sprite(self) -> pygame.Surface:
        """Create a sprite for the Player character."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Body (blue and gold uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (5, 4, 6, 8))  # Torso (blue)
        
        # Head (skin tone)
        pygame.draw.circle(sprite, (255, 200, 150), (8, 4), 3)
        
        # Arms (blue uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (3, 5, 2, 4))  # Left arm
        pygame.draw.rect(sprite, (46, 94, 170), (11, 5, 2, 4))  # Right arm
        
        # Legs (blue uniform)
        pygame.draw.rect(sprite, (46, 94, 170), (6, 12, 2, 4))  # Left leg
        pygame.draw.rect(sprite, (46, 94, 170), (8, 12, 2, 4))  # Right leg
        
        # Laptop (showing they're tech-savvy)
        pygame.draw.rect(sprite, (50, 50, 50), (2, 10, 3, 2))  # Laptop base
        pygame.draw.rect(sprite, (30, 30, 30), (2, 8, 3, 2))   # Laptop screen
        
        return sprite
        
    def get_sprite(self, character_name: str) -> pygame.Surface:
        """Get a character sprite by name.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Character sprite surface
        """
        return self.sprites.get(character_name, self._create_default_sprite())
        
    def _create_default_sprite(self) -> pygame.Surface:
        """Create a default sprite for unknown characters."""
        sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.rect(sprite, (100, 100, 100), (4, 4, 8, 8))
        pygame.draw.circle(sprite, (150, 150, 150), (8, 4), 2)
        return sprite
        
    def get_all_sprites(self) -> Dict[str, pygame.Surface]:
        """Get all character sprites.
        
        Returns:
            Dictionary of all character sprites
        """
        return self.sprites.copy()
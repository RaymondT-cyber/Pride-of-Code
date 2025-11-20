"""
Sound Manager - Audio system for Code of Pride.

This module handles all audio playback, including sound effects and music.
"""

import pygame
import os
import math
from typing import Dict, Optional
from config import AUDIO_ENABLED, DEFAULT_VOLUME, ASSETS_DIR


class SoundManager:
    """Manages sound effects and music playback."""
    
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = DEFAULT_VOLUME
        self.sfx_volume = DEFAULT_VOLUME
        self.music_playing = False
        
        # Initialize mixer
        if AUDIO_ENABLED:
            pygame.mixer.init()
            
        # Load default sounds
        self._load_default_sounds()
        
    def _load_default_sounds(self):
        """Load default sound effects."""
        # Create placeholder sounds since we don't have actual audio files
        if not AUDIO_ENABLED:
            return
            
        # Create simple tone-based sounds
        self._create_placeholder_sounds()
        
    def _create_placeholder_sounds(self):
        """Create simple placeholder sounds using square waves."""
        if not AUDIO_ENABLED:
            return
            
        # Move sound - short beep
        self.sounds['move'] = self._create_tone_sound(440, 0.1)
        
        # Turn sound - lower beep
        self.sounds['turn'] = self._create_tone_sound(330, 0.1)
        
        # Success sound - ascending notes
        self.sounds['success'] = self._create_tone_sound(523, 0.15)  # C
        # In a real implementation, we would play multiple notes
        
        # Error sound - descending notes
        self.sounds['error'] = self._create_tone_sound(220, 0.2)  # A
        # In a real implementation, we would play multiple notes
        
        # Click sound - short click
        self.sounds['click'] = self._create_tone_sound(880, 0.05)
        
    def _create_tone_sound(self, frequency: int, duration: float) -> pygame.mixer.Sound:
        """Create a simple tone sound.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            
        Returns:
            pygame.mixer.Sound object
        """
        if not AUDIO_ENABLED:
            return None
            
        # Create a simple square wave
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create waveform using Python arrays instead of numpy
        import array
        samples = array.array('h')  # Signed 16-bit integers
        
        # Generate square wave
        period = int(sample_rate / frequency)
        for i in range(frames):
            if (i % period) < (period / 2):
                value = 4096  # Amplitude
            else:
                value = -4096
            samples.append(value)  # Left channel
            samples.append(value)  # Right channel
            
        # Convert to sound
        sound = pygame.mixer.Sound(buffer=samples)
        return sound
        
    def play_sound(self, sound_name: str, volume: float = None):
        """Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play
            volume: Volume level (0.0 to 1.0), defaults to sfx_volume
        """
        if not AUDIO_ENABLED or sound_name not in self.sounds:
            return
            
        sound = self.sounds[sound_name]
        if volume is not None:
            sound.set_volume(volume)
        else:
            sound.set_volume(self.sfx_volume)
            
        sound.play()
        
    def play_move_sound(self):
        """Play the move sound effect."""
        self.play_sound('move')
        
    def play_turn_sound(self):
        """Play the turn sound effect."""
        self.play_sound('turn')
        
    def play_success_sound(self):
        """Play the success sound effect."""
        self.play_sound('success')
        
    def play_error_sound(self):
        """Play the error sound effect."""
        self.play_sound('error')
        
    def play_click_sound(self):
        """Play the click sound effect."""
        self.play_sound('click')
        
    def set_music_volume(self, volume: float):
        """Set the music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if AUDIO_ENABLED:
            pygame.mixer.music.set_volume(self.music_volume)
            
    def set_sfx_volume(self, volume: float):
        """Set the sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        
    def load_music(self, filename: str):
        """Load background music.
        
        Args:
            filename: Path to music file
        """
        if not AUDIO_ENABLED:
            return
            
        try:
            pygame.mixer.music.load(filename)
        except pygame.error:
            print(f"Could not load music file: {filename}")
            
    def play_music(self, loops: int = -1):
        """Play background music.
        
        Args:
            loops: Number of times to loop (-1 for infinite)
        """
        if not AUDIO_ENABLED:
            return
            
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)
        self.music_playing = True
        
    def stop_music(self):
        """Stop background music."""
        if not AUDIO_ENABLED:
            return
            
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def pause_music(self):
        """Pause background music."""
        if not AUDIO_ENABLED or not self.music_playing:
            return
            
        pygame.mixer.music.pause()
        
    def resume_music(self):
        """Resume background music."""
        if not AUDIO_ENABLED:
            return
            
        pygame.mixer.music.unpause()
        
    def is_music_playing(self) -> bool:
        """Check if music is currently playing.
        
        Returns:
            True if music is playing, False otherwise
        """
        if not AUDIO_ENABLED:
            return False
            
        return pygame.mixer.music.get_busy()
"""
Story Engine - Narrative progression for Code of Pride.

This module implements the story engine that drives the narrative
progression of the campaign mode.
"""

import pygame
from typing import List, Dict, Optional
from story.dialogue import DialogueSystem


class StoryEngine:
    """Manages the narrative progression of the game."""
    
    def __init__(self):
        self.dialogue_system = DialogueSystem()
        self.current_story_beat = 'preseason'
        self.current_week = 1
        self.story_progress = []
        
        # Story beats with their narrative content
        self.story_beats = {
            'preseason': {
                'title': 'Preseason Practice',
                'description': 'Getting ready for the season ahead',
                'key_events': [
                    'Introduction to the Pride of Casa Grande',
                    'Meeting the team and staff',
                    'Learning the basics of drill programming'
                ],
                'characters': ['drum_major', 'band_director'],
                'themes': ['introduction', 'learning', 'teamwork']
            },
            'first_game': {
                'title': 'First Game',
                'description': 'Debut performance at Casa Grande High',
                'key_events': [
                    'Nervous energy before the performance',
                    'Executing the first drill successfully',
                    'Positive feedback from the crowd'
                ],
                'characters': ['drum_major', 'band_director'],
                'themes': ['debut', 'performance', 'confidence']
            },
            'rivalry': {
                'title': 'Rivalry Week',
                'description': 'Showdown against Desert Ridge',
                'key_events': [
                    'Intense practice sessions',
                    'Developing complex formations',
                    'Competitive spirit and determination'
                ],
                'characters': ['drum_major', 'brass_leader', 'percussion_leader'],
                'themes': ['competition', 'challenge', 'growth']
            },
            'homecoming': {
                'title': 'Homecoming Spectacular',
                'description': 'Special performance for homecoming week',
                'key_events': [
                    'Creating a special routine for homecoming',
                    'Involving the entire school community',
                    'Showcasing advanced programming techniques'
                ],
                'characters': ['drum_major', 'guard_leader', 'woodwind_leader'],
                'themes': ['community', 'celebration', 'showcase']
            },
            'midseason': {
                'title': 'Midseason Review',
                'description': 'Halfway point of the season',
                'key_events': [
                    'Reflecting on progress made so far',
                    'Addressing areas for improvement',
                    'Preparing for the challenging second half'
                ],
                'characters': ['band_director', 'drum_major'],
                'themes': ['reflection', 'improvement', 'preparation']
            },
            'playoffs': {
                'title': 'Playoff Push',
                'description': 'Competing in regional playoffs',
                'key_events': [
                    'Elevated level of competition',
                    'Implementing advanced programming concepts',
                    'Team unity under pressure'
                ],
                'characters': ['band_director', 'drum_major', 'section_leaders'],
                'themes': ['competition', 'advanced_skills', 'teamwork']
            },
            'championship': {
                'title': 'State Championship',
                'description': 'Final performance of the season',
                'key_events': [
                    'The culmination of the entire season',
                    'Using all learned skills for the final challenge',
                    'Celebration of achievements and growth'
                ],
                'characters': ['band_director', 'drum_major', 'entire_team'],
                'themes': ['culmination', 'mastery', 'celebration']
            }
        }
        
    def get_story_beat_info(self, story_beat: str) -> Optional[Dict]:
        """Get information about a specific story beat.
        
        Args:
            story_beat: Story beat identifier
            
        Returns:
            Dictionary with story beat information or None
        """
        return self.story_beats.get(story_beat)
        
    def get_story_beat_text(self, story_beat: str, week: int) -> str:
        """Get narrative text for a story beat.
        
        Args:
            story_beat: Story beat identifier
            week: Current week number
            
        Returns:
            Narrative text for the story beat
        """
        beat_info = self.story_beats.get(story_beat)
        if not beat_info:
            return "Another week of practice and progress..."
            
        # Create a narrative summary
        narrative = f"{beat_info['title']}\n\n"
        narrative += f"{beat_info['description']}\n\n"
        narrative += "This week's key moments:\n"
        for i, event in enumerate(beat_info['key_events'], 1):
            narrative += f"{i}. {event}\n"
            
        return narrative
        
    def get_weekly_narrative(self, week: int, story_beat: str) -> List[str]:
        """Get the weekly narrative dialogue.
        
        Args:
            week: Week number
            story_beat: Current story beat
            
        Returns:
            List of dialogue lines for the week
        """
        return self.dialogue_system.get_story_beat_dialogue(story_beat, week)
        
    def advance_story(self, new_beat: str, week: int):
        """Advance the story to a new beat.
        
        Args:
            new_beat: New story beat identifier
            week: Current week number
        """
        if new_beat in self.story_beats:
            self.current_story_beat = new_beat
            self.current_week = week
            self.story_progress.append({
                'beat': new_beat,
                'week': week,
                'timestamp': pygame.time.get_ticks()
            })
            
    def get_character_introduction(self, character: str) -> List[str]:
        """Get introduction dialogue for a character.
        
        Args:
            character: Character name
            
        Returns:
            List of introduction dialogue lines
        """
        return self.dialogue_system.get_character_introduction(character)
        
    def get_character_dialogue(self, character: str, dialogue_type: str) -> str:
        """Get a random dialogue line for a character.
        
        Args:
            character: Character name
            dialogue_type: Type of dialogue
            
        Returns:
            Dialogue line
        """
        return self.dialogue_system.get_character_dialogue(character, dialogue_type)
        
    def start_dialogue_sequence(self, character: str, dialogue_sequence: List[str]):
        """Start a dialogue sequence.
        
        Args:
            character: Character speaking
            dialogue_sequence: List of dialogue lines
        """
        self.dialogue_system.start_dialogue_sequence(character, dialogue_sequence)
        
    def advance_dialogue(self) -> bool:
        """Advance to the next line in the dialogue sequence.
        
        Returns:
            True if there's more dialogue, False if sequence is complete
        """
        return self.dialogue_system.advance_dialogue()
        
    def get_current_dialogue(self) -> Optional[Dict]:
        """Get the current dialogue information.
        
        Returns:
            Dictionary with current dialogue information or None
        """
        return self.dialogue_system.get_current_dialogue()
        
    def is_dialogue_complete(self) -> bool:
        """Check if the current dialogue sequence is complete.
        
        Returns:
            True if dialogue is complete, False otherwise
        """
        return self.dialogue_system.is_dialogue_complete()
        
    def draw_dialogue_box(self, surface: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw the current dialogue in a box.
        
        Args:
            surface: Surface to draw on
            x, y: Position of the dialogue box
            width, height: Dimensions of the dialogue box
        """
        self.dialogue_system.draw_dialogue_box(surface, x, y, width, height)
        
    def get_story_progress(self) -> List[Dict]:
        """Get the story progress history.
        
        Returns:
            List of story progress entries
        """
        return self.story_progress.copy()
        
    def get_available_characters(self, story_beat: str) -> List[str]:
        """Get characters available for a story beat.
        
        Args:
            story_beat: Story beat identifier
            
        Returns:
            List of available character names
        """
        beat_info = self.story_beats.get(story_beat)
        if not beat_info:
            return ['drum_major', 'band_director']
        return beat_info.get('characters', ['drum_major', 'band_director'])
        
    def get_story_themes(self, story_beat: str) -> List[str]:
        """Get themes for a story beat.
        
        Args:
            story_beat: Story beat identifier
            
        Returns:
            List of theme keywords
        """
        beat_info = self.story_beats.get(story_beat)
        if not beat_info:
            return ['learning', 'progress']
        return beat_info.get('themes', ['learning', 'progress'])
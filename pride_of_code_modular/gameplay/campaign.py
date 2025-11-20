"""
Campaign Mode - Story-driven progression for Code of Pride.

This module implements the story-driven campaign mode where players 
follow the "Pride of Casa Grande" through a full competitive season.
"""

import pygame
from typing import List, Dict, Optional
from gameplay.lessons import LessonManager
from gameplay.scoring import PridePoints
from story.engine import StoryEngine
from config import DIFFICULTY_LEVELS


class CampaignMode:
    """Manages the story-driven campaign mode."""
    
    def __init__(self):
        self.lesson_manager = LessonManager()
        self.scorer = PridePoints()
        self.story_engine = StoryEngine()
        
        # Campaign state
        self.current_week = 1
        self.total_weeks = 10
        self.difficulty = 'beginner'
        self.unlocked_lessons = set()
        self.completed_lessons = set()
        self.campaign_score = 0.0
        
        # Story progression
        self.current_story_beat = 0
        self.story_beats = [
            "preseason",
            "first_game",
            "rivalry",
            "homecoming",
            "midseason",
            "playoffs",
            "championship"
        ]
        
        # Team stats
        self.team_stats = {
            'wins': 0,
            'losses': 0,
            'streak': 0,
            'max_streak': 0,
            'points_for': 0,
            'points_against': 0
        }
        
        # Unlock initial lessons
        self._unlock_initial_lessons()
        
    def _unlock_initial_lessons(self):
        """Unlock the initial lessons for the campaign."""
        # Always unlock the first lesson
        first_lesson = self.lesson_manager.get_lesson(1, 1)
        if first_lesson:
            self.unlocked_lessons.add((1, 1))
            
    def start_week(self, week: int) -> bool:
        """Start a new week in the campaign.
        
        Args:
            week: Week number to start
            
        Returns:
            True if week started successfully, False otherwise
        """
        if week < 1 or week > self.total_weeks:
            return False
            
        self.current_week = week
        
        # Unlock lessons for this week
        self._unlock_week_lessons(week)
        
        # Advance story
        self._advance_story(week)
        
        return True
        
    def _unlock_week_lessons(self, week: int):
        """Unlock lessons for the specified week.
        
        Args:
            week: Week number
        """
        # Unlock lessons based on week and difficulty
        band_size = DIFFICULTY_LEVELS[self.difficulty]['band_size']
        
        # For beginner difficulty, unlock one lesson per week
        if self.difficulty == 'beginner':
            module = (week - 1) // 2 + 1  # 2 weeks per module
            lesson = ((week - 1) % 2) + 1  # Lesson 1 or 2
            
            if module <= 5 and lesson <= 3:  # Max 5 modules, 3 lessons each
                self.unlocked_lessons.add((module, lesson))
                
        # For other difficulties, unlock more lessons
        else:
            # Unlock all lessons up to current week's module
            current_module = (week - 1) // 2 + 1
            for mod in range(1, min(current_module + 1, 6)):
                for les in range(1, 4):  # 3 lessons per module
                    self.unlocked_lessons.add((mod, les))
                    
    def _advance_story(self, week: int):
        """Advance the story based on the current week.
        
        Args:
            week: Current week number
        """
        # Map weeks to story beats
        story_map = {
            1: "preseason",
            2: "first_game",
            3: "rivalry",
            4: "homecoming",
            5: "midseason",
            6: "rivalry",  # Second rivalry game
            7: "playoffs",
            8: "playoffs",
            9: "championship",
            10: "championship"  # Championship if made it
        }
        
        if week in story_map:
            self.current_story_beat = self.story_beats.index(story_map[week])
            
    def is_lesson_unlocked(self, module: int, lesson: int) -> bool:
        """Check if a lesson is unlocked.
        
        Args:
            module: Module number
            lesson: Lesson number
            
        Returns:
            True if lesson is unlocked, False otherwise
        """
        return (module, lesson) in self.unlocked_lessons
        
    def is_lesson_completed(self, module: int, lesson: int) -> bool:
        """Check if a lesson is completed.
        
        Args:
            module: Module number
            lesson: Lesson number
            
        Returns:
            True if lesson is completed, False otherwise
        """
        return (module, lesson) in self.completed_lessons
        
    def complete_lesson(self, module: int, lesson: int, score: float) -> bool:
        """Mark a lesson as completed.
        
        Args:
            module: Module number
            lesson: Lesson number
            score: Score achieved in the lesson
            
        Returns:
            True if lesson was marked as completed, False otherwise
        """
        if not self.is_lesson_unlocked(module, lesson):
            return False
            
        self.completed_lessons.add((module, lesson))
        self.campaign_score += score
        
        # Update streak
        if score > 0:
            self.team_stats['streak'] += 1
            self.team_stats['max_streak'] = max(self.team_stats['max_streak'], 
                                               self.team_stats['streak'])
            self.team_stats['points_for'] += int(score)
        else:
            self.team_stats['streak'] = 0
            
        return True
        
    def get_week_schedule(self) -> Dict:
        """Get the schedule for the current week.
        
        Returns:
            Dictionary with schedule information
        """
        schedule = {
            'week': self.current_week,
            'story_beat': self.story_beats[self.current_story_beat],
            'lessons': [],
            'opponent': self._get_opponent(self.current_week),
            'location': self._get_location(self.current_week)
        }
        
        # Add unlocked lessons for this week
        week_module = (self.current_week - 1) // 2 + 1
        for lesson in range(1, 4):
            if self.is_lesson_unlocked(week_module, lesson):
                lesson_info = self.lesson_manager.get_lesson(week_module, lesson)
                if lesson_info:
                    schedule['lessons'].append({
                        'module': week_module,
                        'lesson': lesson,
                        'title': lesson_info['title'],
                        'completed': self.is_lesson_completed(week_module, lesson)
                    })
                    
        return schedule
        
    def _get_opponent(self, week: int) -> str:
        """Get the opponent for the specified week.
        
        Args:
            week: Week number
            
        Returns:
            Opponent team name
        """
        opponents = {
            1: "Cactus High",
            2: "Mountain View",
            3: "Desert Ridge",
            4: "Boulder Creek",
            5: "Grand Canyon Prep",
            6: "Desert Ridge",  # Rivalry rematch
            7: "Region 4 Runner-up",
            8: "Region 4 Champion",
            9: "State Semifinalist",
            10: "State Champion"
        }
        
        return opponents.get(week, "TBD")
        
    def _get_location(self, week: int) -> str:
        """Get the location for the specified week.
        
        Args:
            week: Week number
            
        Returns:
            Game location
        """
        locations = {
            1: "Home",
            2: "Away",
            3: "Home",
            4: "Home",
            5: "Away",
            6: "Away",  # Rivalry rematch
            7: "Neutral Site",
            8: "Home",
            9: "State Stadium",
            10: "Championship Stadium"
        }
        
        return locations.get(week, "Home")
        
    def get_campaign_progress(self) -> Dict:
        """Get overall campaign progress.
        
        Returns:
            Dictionary with progress information
        """
        total_lessons = len(self.unlocked_lessons)
        completed_lessons = len(self.completed_lessons)
        
        progress = {
            'current_week': self.current_week,
            'total_weeks': self.total_weeks,
            'lessons_completed': completed_lessons,
            'lessons_unlocked': total_lessons,
            'completion_percentage': (completed_lessons / max(1, total_lessons)) * 100,
            'campaign_score': self.campaign_score,
            'team_stats': self.team_stats.copy(),
            'current_story_beat': self.story_beats[self.current_story_beat]
        }
        
        return progress
        
    def get_story_text(self) -> str:
        """Get the current story text.
        
        Returns:
            Current story text
        """
        return self.story_engine.get_story_beat_text(
            self.story_beats[self.current_story_beat], 
            self.current_week
        )
        
    def set_difficulty(self, difficulty: str):
        """Set the campaign difficulty.
        
        Args:
            difficulty: Difficulty level ('beginner', 'intermediate', 'advanced')
        """
        if difficulty in DIFFICULTY_LEVELS:
            self.difficulty = difficulty
            
    def get_difficulty(self) -> str:
        """Get the current difficulty level.
        
        Returns:
            Current difficulty level
        """
        return self.difficulty
        
    def reset_campaign(self):
        """Reset the campaign progress."""
        self.current_week = 1
        self.unlocked_lessons.clear()
        self.completed_lessons.clear()
        self.campaign_score = 0.0
        self.current_story_beat = 0
        
        # Reset team stats
        self.team_stats = {
            'wins': 0,
            'losses': 0,
            'streak': 0,
            'max_streak': 0,
            'points_for': 0,
            'points_against': 0
        }
        
        # Unlock initial lessons
        self._unlock_initial_lessons()
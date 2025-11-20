"""
Scoring System - Pride Points for Code of Pride.

This module implements the "Pride Points" scoring system that rewards players 
for completing challenges efficiently and creatively.
"""

import pygame
from typing import Dict, List, Tuple
from config import COLOR_BLUE, COLOR_GOLD, COLOR_BG, COLOR_TEXT


class PridePoints:
    """A scoring system that rewards efficient and creative coding."""
    
    def __init__(self):
        self.total_points = 0.0
        self.multiplier = 1.0
        self.streak = 0
        self.max_streak = 0
        
        # Scoring categories
        self.scores = {
            'correct_formation': 0,
            'efficient_code': 0,
            'creativity': 0,
            'speed_bonus': 0,
            'streak_bonus': 0
        }
        
        # Font for display
        self.font_medium = pygame.font.SysFont('arial', 16, bold=True)
        self.font_small = pygame.font.SysFont('arial', 12)
        
        # Colors
        self.colors = {
            'background': (30, 30, 40, 180),  # Semi-transparent
            'border': COLOR_BLUE,
            'text': COLOR_TEXT,
            'highlight': COLOR_GOLD,
            'positive': (100, 200, 100),
            'negative': (200, 100, 100)
        }
        
    def add_points(self, points: float, reason: str = "", show_feedback: bool = True):
        """Add points to the total score.
        
        Args:
            points: Number of points to add (can be negative)
            reason: Reason for the points (for feedback)
            show_feedback: Whether to show visual feedback
        """
        actual_points = points * self.multiplier
        self.total_points += actual_points
        
        # Update streak
        if actual_points > 0:
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
        else:
            self.streak = 0
            
        # Update multiplier based on streak
        self.multiplier = 1.0 + min(self.streak * 0.05, 0.5)  # Max 50% bonus
        
        # Store reason for display
        if reason:
            # Simple categorization based on reason
            if "formation" in reason.lower():
                self.scores['correct_formation'] += actual_points
            elif "efficient" in reason.lower() or "loop" in reason.lower():
                self.scores['efficient_code'] += actual_points
            elif "creative" in reason.lower() or "unique" in reason.lower():
                self.scores['creativity'] += actual_points
            elif "fast" in reason.lower() or "quick" in reason.lower():
                self.scores['speed_bonus'] += actual_points
            elif "streak" in reason.lower():
                self.scores['streak_bonus'] += actual_points
                
        return actual_points
        
    def reset_streak(self):
        """Reset the current streak."""
        self.streak = 0
        self.multiplier = 1.0
        
    def reset(self):
        """Reset all scores."""
        self.total_points = 0.0
        self.multiplier = 1.0
        self.streak = 0
        self.max_streak = 0
        for key in self.scores:
            self.scores[key] = 0
            
    def get_score_breakdown(self) -> Dict[str, float]:
        """Get a breakdown of scores by category.
        
        Returns:
            Dictionary with score categories and values
        """
        return self.scores.copy()
        
    def draw(self, surface: pygame.Surface, x: int, y: int):
        """Draw the score display.
        
        Args:
            surface: Surface to draw on
            x, y: Position to draw at
        """
        # Draw background
        width, height = 200, 120
        bg_rect = pygame.Rect(x, y, width, height)
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill(self.colors['background'])
        surface.blit(s, (x, y))
        pygame.draw.rect(surface, self.colors['border'], bg_rect, 2)
        
        # Draw title
        title = self.font_medium.render("Pride Points", True, self.colors['highlight'])
        surface.blit(title, (x + 10, y + 5))
        
        # Draw total points
        points_text = f"Total: {self.total_points:.1f}"
        text = self.font_medium.render(points_text, True, self.colors['text'])
        surface.blit(text, (x + 10, y + 30))
        
        # Draw multiplier
        if self.multiplier > 1.0:
            mult_text = f"Multiplier: x{self.multiplier:.2f}"
            text = self.font_small.render(mult_text, True, self.colors['highlight'])
            surface.blit(text, (x + 10, y + 55))
            
        # Draw streak
        streak_text = f"Streak: {self.streak}"
        text = self.font_small.render(streak_text, True, self.colors['text'])
        surface.blit(text, (x + 10, y + 75))
        
    def draw_detailed(self, surface: pygame.Surface, x: int, y: int):
        """Draw a detailed score breakdown.
        
        Args:
            surface: Surface to draw on
            x, y: Position to draw at
        """
        # Draw background
        width, height = 250, 180
        bg_rect = pygame.Rect(x, y, width, height)
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill(self.colors['background'])
        surface.blit(s, (x, y))
        pygame.draw.rect(surface, self.colors['border'], bg_rect, 2)
        
        # Draw title
        title = self.font_medium.render("Score Breakdown", True, self.colors['highlight'])
        surface.blit(title, (x + 10, y + 5))
        
        # Draw each category
        y_offset = 35
        for category, points in self.scores.items():
            # Format category name
            display_name = category.replace('_', ' ').title()
            # Draw category and points
            cat_text = self.font_small.render(f"{display_name}:", True, self.colors['text'])
            pts_text = self.font_small.render(f"{points:.1f}", True, 
                                            self.colors['positive'] if points >= 0 else self.colors['negative'])
            surface.blit(cat_text, (x + 10, y + y_offset))
            surface.blit(pts_text, (x + width - 50, y + y_offset))
            y_offset += 20
            
        # Draw total
        pygame.draw.line(surface, self.colors['border'], 
                        (x + 10, y + y_offset), (x + width - 10, y + y_offset), 1)
        y_offset += 10
        total_text = self.font_medium.render(f"Total: {self.total_points:.1f}", True, self.colors['highlight'])
        surface.blit(total_text, (x + 10, y + y_offset))
        
        # Draw multiplier and streak
        y_offset += 25
        mult_text = f"Multiplier: x{self.multiplier:.2f}"
        streak_text = f"Streak: {self.streak} (Max: {self.max_streak})"
        mult_surf = self.font_small.render(mult_text, True, self.colors['text'])
        streak_surf = self.font_small.render(streak_text, True, self.colors['text'])
        surface.blit(mult_surf, (x + 10, y + y_offset))
        surface.blit(streak_surf, (x + 10, y + y_offset + 20))
        
    def calculate_efficiency_score(self, code_lines: int, expected_lines: int) -> float:
        """Calculate points based on code efficiency.
        
        Args:
            code_lines: Number of lines in player's code
            expected_lines: Expected number of lines
            
        Returns:
            Points awarded for efficiency
        """
        if code_lines <= 0:
            return 0
            
        # Base points for completing the challenge
        base_points = 20.0
        
        # Efficiency bonus - fewer lines = more points
        if code_lines <= expected_lines:
            # Bonus for using fewer or expected lines
            efficiency_ratio = expected_lines / max(code_lines, 1)
            efficiency_bonus = base_points * (efficiency_ratio - 1) * 0.5
            return base_points + max(0, efficiency_bonus)
        else:
            # Penalty for using more lines
            excess_ratio = code_lines / expected_lines
            penalty = base_points * (1 - 1/excess_ratio) * 0.3
            return max(5.0, base_points - penalty)
            
    def calculate_creativity_score(self, code_complexity: int) -> float:
        """Calculate points based on code creativity/complexity.
        
        Args:
            code_complexity: Measure of code complexity (function count, etc.)
            
        Returns:
            Points awarded for creativity
        """
        # Base points
        base_points = 10.0
        
        # Bonus for using more complex constructs
        complexity_bonus = min(code_complexity * 2.0, 20.0)
        return base_points + complexity_bonus
        
    def calculate_speed_bonus(self, time_taken: float, expected_time: float) -> float:
        """Calculate bonus points for completing challenges quickly.
        
        Args:
            time_taken: Time taken to complete challenge (seconds)
            expected_time: Expected time to complete challenge
            
        Returns:
            Bonus points for speed
        """
        if time_taken <= 0:
            return 0
            
        # Base bonus
        base_bonus = 15.0
        
        # Time ratio - faster = more points
        if time_taken <= expected_time:
            time_ratio = expected_time / max(time_taken, 0.1)
            speed_bonus = base_bonus * (time_ratio - 1) * 0.7
            return base_bonus + max(0, speed_bonus)
        else:
            # Penalty for taking too long
            time_ratio = time_taken / expected_time
            penalty = base_bonus * (1 - 1/time_ratio) * 0.4
            return max(2.0, base_bonus - penalty)
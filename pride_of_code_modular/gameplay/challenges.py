"""
Challenge Mode - Daily coding challenges for Code of Pride.

This module implements the challenge mode with daily coding challenges
that focus on specific programming concepts or tricky drill design problems.
"""

import pygame
import random
import datetime
from typing import List, Dict, Optional
from gameplay.scoring import PridePoints


class ChallengeMode:
    """Manages the daily challenge mode."""
    
    def __init__(self):
        self.scorer = PridePoints()
        self.challenges = self._generate_challenges()
        self.completed_challenges = set()
        self.current_challenge = None
        self.challenge_start_time = 0
        
        # Leaderboard
        self.leaderboard = []
        
    def _generate_challenges(self) -> List[Dict]:
        """Generate a list of daily challenges.
        
        Returns:
            List of challenge dictionaries
        """
        challenges = [
            {
                'id': 1,
                'title': 'Basic Movement',
                'description': 'Move a single band member to a specific position',
                'difficulty': 'beginner',
                'expected_lines': 3,
                'time_limit': 120,  # seconds
                'points': 20,
                'setup_code': '# Create a single band member at position (20, 20)\n'
                             'member = band.get_member(0)\n',
                'solution_check': 'member.x == 50 and member.y == 30'
            },
            {
                'id': 2,
                'title': 'Line Formation',
                'description': 'Form a line with 5 band members',
                'difficulty': 'beginner',
                'expected_lines': 5,
                'time_limit': 180,
                'points': 30,
                'setup_code': '# Create 5 band members\n'
                             'members = band.get_all_members()[:5]\n',
                'solution_check': 'len(members) == 5 and _is_line_formation(members)'
            },
            {
                'id': 3,
                'title': 'Circle Formation',
                'description': 'Arrange 8 band members in a perfect circle',
                'difficulty': 'intermediate',
                'expected_lines': 8,
                'time_limit': 240,
                'points': 40,
                'setup_code': '# Create 8 band members\n'
                             'members = band.get_all_members()[:8]\n',
                'solution_check': 'len(members) == 8 and _is_circle_formation(members)'
            },
            {
                'id': 4,
                'title': 'Section Control',
                'description': 'Move all brass members to form a block',
                'difficulty': 'intermediate',
                'expected_lines': 6,
                'time_limit': 200,
                'points': 35,
                'setup_code': '# Get all brass members\n'
                             'brass_members = band.get_section("brass")\n',
                'solution_check': 'len(brass_members) > 0 and _is_block_formation(brass_members)'
            },
            {
                'id': 5,
                'title': 'Complex Pattern',
                'description': 'Create a complex pattern using loops and conditions',
                'difficulty': 'advanced',
                'expected_lines': 15,
                'time_limit': 300,
                'points': 50,
                'setup_code': '# Create 12 band members\n'
                             'members = band.get_all_members()[:12]\n'
                             '# Add some conditions\n'
                             'for i, member in enumerate(members):\n'
                             '    if i % 2 == 0:\n'
                             '        member.instrument = "trumpet"\n'
                             '    else:\n'
                             '        member.instrument = "trombone"\n',
                'solution_check': 'len(members) == 12 and _is_complex_pattern(members)'
            }
        ]
        
        return challenges
        
    def get_daily_challenge(self) -> Dict:
        """Get today's daily challenge.
        
        Returns:
            Challenge dictionary for today
        """
        # In a real implementation, we would use the actual date
        # For now, we'll just rotate through challenges
        today = datetime.date.today()
        days_since_epoch = (today - datetime.date(2024, 1, 1)).days
        challenge_index = days_since_epoch % len(self.challenges)
        
        self.current_challenge = self.challenges[challenge_index].copy()
        self.challenge_start_time = pygame.time.get_ticks() / 1000.0
        
        return self.current_challenge
        
    def get_random_challenge(self, difficulty: str = None) -> Dict:
        """Get a random challenge, optionally filtered by difficulty.
        
        Args:
            difficulty: Difficulty level to filter by
            
        Returns:
            Random challenge dictionary
        """
        if difficulty:
            filtered = [c for c in self.challenges if c['difficulty'] == difficulty]
            if filtered:
                self.current_challenge = random.choice(filtered).copy()
            else:
                self.current_challenge = random.choice(self.challenges).copy()
        else:
            self.current_challenge = random.choice(self.challenges).copy()
            
        self.challenge_start_time = pygame.time.get_ticks() / 1000.0
        return self.current_challenge
        
    def submit_solution(self, code: str) -> Dict:
        """Submit a solution for the current challenge.
        
        Args:
            code: Code solution to evaluate
            
        Returns:
            Dictionary with results
        """
        if not self.current_challenge:
            return {'success': False, 'message': 'No challenge selected'}
            
        # Calculate time taken
        time_taken = (pygame.time.get_ticks() / 1000.0) - self.challenge_start_time
        
        # Check if solution is correct (simplified check)
        # In a real implementation, we would execute the code and verify the result
        is_correct = self._check_solution(code)
        
        # Calculate score
        points = 0
        if is_correct:
            # Base points
            points = self.current_challenge['points']
            
            # Time bonus
            time_limit = self.current_challenge['time_limit']
            if time_taken < time_limit:
                time_bonus = (time_limit - time_taken) / time_limit * 10
                points += time_bonus
                
            # Add to scorer
            self.scorer.add_points(points, "Challenge completed")
            
            # Mark as completed
            self.completed_challenges.add(self.current_challenge['id'])
            
        # Return results
        return {
            'success': is_correct,
            'points': points,
            'time_taken': time_taken,
            'message': 'Challenge completed!' if is_correct else 'Solution incorrect'
        }
        
    def _check_solution(self, code: str) -> bool:
        """Check if the solution is correct.
        
        Args:
            code: Code to check
            
        Returns:
            True if solution is correct, False otherwise
        """
        # This is a simplified check
        # In a real implementation, we would execute the code and verify the result
        # against the challenge requirements
        
        # For now, we'll just check if the code contains some expected elements
        required_elements = [
            'band.move_to',
            'band.form_line',
            'band.form_circle',
            'band.form_block'
        ]
        
        # Check for at least one required element
        for element in required_elements:
            if element in code:
                return True
                
        return False
        
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get the challenge leaderboard.
        
        Args:
            limit: Number of top scores to return
            
        Returns:
            List of leaderboard entries
        """
        # Sort leaderboard by score (descending)
        sorted_leaderboard = sorted(
            self.leaderboard, 
            key=lambda x: x['score'], 
            reverse=True
        )
        
        return sorted_leaderboard[:limit]
        
    def add_to_leaderboard(self, name: str, score: float):
        """Add an entry to the leaderboard.
        
        Args:
            name: Player name
            score: Score achieved
        """
        entry = {
            'name': name,
            'score': score,
            'date': datetime.date.today().isoformat()
        }
        
        self.leaderboard.append(entry)
        
        # Keep only top 100 scores
        if len(self.leaderboard) > 100:
            self.leaderboard = sorted(
                self.leaderboard, 
                key=lambda x: x['score'], 
                reverse=True
            )[:100]
            
    def get_completed_count(self) -> int:
        """Get the number of completed challenges.
        
        Returns:
            Number of completed challenges
        """
        return len(self.completed_challenges)
        
    def get_total_count(self) -> int:
        """Get the total number of challenges.
        
        Returns:
            Total number of challenges
        """
        return len(self.challenges)
        
    def get_completion_percentage(self) -> float:
        """Get the completion percentage.
        
        Returns:
            Completion percentage
        """
        if not self.challenges:
            return 0.0
        return (len(self.completed_challenges) / len(self.challenges)) * 100
        
    def reset_progress(self):
        """Reset challenge progress."""
        self.completed_challenges.clear()
        self.leaderboard.clear()
        self.current_challenge = None
        
    def _is_line_formation(self, members) -> bool:
        """Check if members form a line (simplified)."""
        # This would be implemented with actual coordinate checking
        return len(members) >= 2
        
    def _is_circle_formation(self, members) -> bool:
        """Check if members form a circle (simplified)."""
        # This would be implemented with actual coordinate checking
        return len(members) >= 3
        
    def _is_block_formation(self, members) -> bool:
        """Check if members form a block (simplified)."""
        # This would be implemented with actual coordinate checking
        return len(members) >= 4
        
    def _is_complex_pattern(self, members) -> bool:
        """Check if members form a complex pattern (simplified)."""
        # This would be implemented with actual coordinate checking
        return len(members) >= 5
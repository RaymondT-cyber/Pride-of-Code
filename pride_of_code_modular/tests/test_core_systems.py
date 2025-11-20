"""
Test Core Systems - Unit tests for Code of Pride.

This module contains unit tests for the core systems of the game.
"""

import unittest
import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gameplay.band_api import BandAPI, BandMember
from gameplay.code_executor import CodeExecutor
from ui.editor import CodeEditor
from ui.field_view import FieldView
from gameplay.scoring import PridePoints
from gameplay.lessons import LessonManager
from gameplay.campaign import CampaignMode
from gameplay.challenges import ChallengeMode
from gameplay.sandbox import SandboxMode
from story.engine import StoryEngine


class TestBandAPI(unittest.TestCase):
    """Test the Band API functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.band_api = BandAPI()
        self.band_api.create_band(8)
        
    def test_create_band(self):
        """Test creating a band."""
        self.assertEqual(len(self.band_api.members), 8)
        # With 8 members, we get 4 brass and 4 woodwind (based on the fixed sections list)
        self.assertEqual(len(self.band_api.sections['brass']), 4)
        self.assertEqual(len(self.band_api.sections['woodwind']), 4)
        
    def test_get_member(self):
        """Test getting a band member."""
        member = self.band_api.get_member(0)
        self.assertIsInstance(member, BandMember)
        self.assertEqual(member.id, 0)
        
    def test_get_section(self):
        """Test getting a section."""
        brass_members = self.band_api.get_section('brass')
        self.assertIsInstance(brass_members, list)
        self.assertGreater(len(brass_members), 0)
        
    def test_move_to(self):
        """Test moving a band member."""
        member = self.band_api.get_member(0)
        original_x, original_y = member.x, member.y
        
        self.band_api.move_to(member, 50, 26)
        self.assertEqual(member.x, 50)
        self.assertEqual(member.y, 26)
        
    def test_form_line(self):
        """Test forming a line."""
        members = self.band_api.get_all_members()[:4]
        self.band_api.form_line(members, 20, 20, 50, 20)
        
        # Check that members are in a line (same y-coordinate)
        for member in members:
            self.assertEqual(member.y, 20)
            
    def test_form_circle(self):
        """Test forming a circle."""
        members = self.band_api.get_all_members()[:6]
        center_x, center_y, radius = 50, 26, 10
        self.band_api.form_circle(members, center_x, center_y, radius)
        
        # Check that members are positioned (basic check)
        for member in members:
            self.assertIsNotNone(member.x)
            self.assertIsNotNone(member.y)


class TestCodeExecutor(unittest.TestCase):
    """Test the Code Executor functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.executor = CodeExecutor()
        
    def test_execute_simple_code(self):
        """Test executing simple code."""
        code = "print('Hello, Band!')"
        success, output = self.executor.execute(code)
        self.assertTrue(success)
        self.assertIn('Hello, Band!', output)
        
    def test_execute_band_code(self):
        """Test executing code that manipulates band members."""
        code = """
member = band.get_member(0)
band.move_to(member, 50, 26)
print(f'Member moved to {member.x}, {member.y}')
"""
        success, output = self.executor.execute(code)
        self.assertTrue(success)
        # The output might not have decimal points if the values are whole numbers
        self.assertIn('Member moved to 50, 26', output)
        
    def test_syntax_error(self):
        """Test handling syntax errors."""
        code = "print('Hello World'"  # Missing closing parenthesis
        success, output = self.executor.execute(code)
        self.assertFalse(success)
        self.assertIn('Syntax Error', output)
        
    def test_name_error(self):
        """Test handling name errors."""
        code = "print(undefined_variable)"
        success, output = self.executor.execute(code)
        self.assertFalse(success)
        self.assertIn('Name Error', output)


class TestCodeEditor(unittest.TestCase):
    """Test the Code Editor functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        rect = pygame.Rect(0, 0, 400, 300)
        self.editor = CodeEditor(rect)
        
    def test_initial_lines(self):
        """Test initial lines are set correctly."""
        self.assertGreater(len(self.editor.lines), 0)
        self.assertIn('Welcome to Code of Pride!', self.editor.lines[0])
        
    def test_insert_text(self):
        """Test inserting text."""
        self.editor.insert_text('test')
        self.assertIn('test', self.editor.lines[0])
        
    def test_new_line(self):
        """Test creating a new line."""
        original_lines = len(self.editor.lines)
        self.editor.new_line()
        self.assertEqual(len(self.editor.lines), original_lines + 1)
        
    def test_backspace(self):
        """Test backspace functionality."""
        self.editor.insert_text('test')
        self.editor.backspace()
        self.assertNotIn('test', self.editor.lines[0])
        
    def test_syntax_check(self):
        """Test syntax checking."""
        # Valid syntax
        self.editor.lines = ['print("Hello")']
        valid, _ = self.editor.check_syntax()
        self.assertTrue(valid)
        
        # Invalid syntax
        self.editor.lines = ['print("Hello"']  # Missing closing parenthesis
        valid, _ = self.editor.check_syntax()
        self.assertFalse(valid)


class TestScoringSystem(unittest.TestCase):
    """Test the Pride Points scoring system."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scorer = PridePoints()
        
    def test_add_points(self):
        """Test adding points."""
        initial_points = self.scorer.total_points
        self.scorer.add_points(10.0, "Test reason")
        self.assertEqual(self.scorer.total_points, initial_points + 10.0)
        
    def test_streak_bonus(self):
        """Test streak bonus calculation."""
        # Add multiple successful points
        self.scorer.add_points(10.0, "Success 1")
        self.scorer.add_points(10.0, "Success 2")
        self.scorer.add_points(10.0, "Success 3")
        
        # Check that multiplier increased
        self.assertGreater(self.scorer.multiplier, 1.0)
        
    def test_reset_streak(self):
        """Test resetting streak."""
        # Build up a streak
        self.scorer.add_points(10.0, "Success")
        self.scorer.add_points(10.0, "Success")
        self.assertGreater(self.scorer.streak, 0)
        
        # Reset streak
        self.scorer.reset_streak()
        self.assertEqual(self.scorer.streak, 0)
        self.assertEqual(self.scorer.multiplier, 1.0)


class TestCurriculum(unittest.TestCase):
    """Test the curriculum implementation."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.lesson_manager = LessonManager()
        
    def test_modules_exist(self):
        """Test that all modules exist."""
        modules = self.lesson_manager.get_all_modules()
        self.assertEqual(len(modules), 5)  # 5 modules total
        
    def test_module_lessons(self):
        """Test that modules have lessons."""
        for module_num in range(1, 6):
            module = self.lesson_manager.get_module(module_num)
            self.assertIsNotNone(module)
            self.assertIn('lessons', module)
            self.assertEqual(len(module['lessons']), 3)  # 3 lessons per module
            
    def test_specific_lesson(self):
        """Test getting a specific lesson."""
        lesson = self.lesson_manager.get_lesson(1, 1)  # Module 1, Lesson 1
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson['title'], 'Meet the Band')


class TestGameModes(unittest.TestCase):
    """Test the game modes."""
    
    def test_campaign_mode(self):
        """Test campaign mode initialization."""
        campaign = CampaignMode()
        self.assertEqual(campaign.current_week, 1)
        self.assertEqual(campaign.difficulty, 'beginner')
        
    def test_challenge_mode(self):
        """Test challenge mode initialization."""
        challenges = ChallengeMode()
        self.assertGreater(len(challenges.challenges), 0)
        
    def test_sandbox_mode(self):
        """Test sandbox mode initialization."""
        sandbox = SandboxMode()
        self.assertEqual(sandbox.band_size, 16)
        self.assertIsNotNone(sandbox.band_api)


class TestStoryEngine(unittest.TestCase):
    """Test the story engine."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.story_engine = StoryEngine()
        
    def test_story_beats(self):
        """Test that story beats exist."""
        beat_info = self.story_engine.get_story_beat_info('preseason')
        self.assertIsNotNone(beat_info)
        self.assertEqual(beat_info['title'], 'Preseason Practice')
        
    def test_character_dialogue(self):
        """Test character dialogue system."""
        dialogue = self.story_engine.get_character_dialogue('drum_major', 'encouragement')
        self.assertIsInstance(dialogue, str)
        self.assertGreater(len(dialogue), 0)


if __name__ == '__main__':
    unittest.main()
"""Lesson definitions and validators for the curriculum.

This module contains the complete 5-module curriculum with lessons,
challenges, and validation logic.
"""

from typing import Dict, Any, Tuple, List
from gameplay.band_api import BandMember


class Lesson:
    """Base class for a lesson."""
    
    def __init__(self, id: str, title: str, description: str, 
                 initial_code: List[str], challenge: str):
        self.id = id
        self.title = title
        self.description = description
        self.initial_code = initial_code
        self.challenge = challenge
        
    def validate(self, band_api) -> Tuple[bool, str]:
        """Validate if the student completed the challenge.
        
        Args:
            band_api: The BandAPI instance after code execution
            
        Returns:
            (success: bool, message: str)
        """
        return True, "Challenge completed!"


class Module1Lesson1(Lesson):
    """Module 1, Lesson 1: Variables & Data Types."""
    
    def __init__(self):
        super().__init__(
            id='week1_lesson1',
            title='Meet the Band - Variables & Data Types',
            description='Learn to create variables and assign values to control band members.',
            initial_code=[
                "# Lesson 1.1: Variables & Data Types",
                "# Challenge: Assign a name and position to a band member",
                "",
                "# Get the first band member",
                "member = members[0]",
                "",
                "# Create variables",
                "member_name = 'Alex'",
                "member_instrument = 'trumpet'",
                "x_position = 50  # 50-yard line",
                "y_position = 26  # Middle of field",
                "",
                "# Move the member to the position",
                "band.move_to(member, x_position, y_position)",
                "",
                "# Print the result",
                "print(f'{member_name} plays {member_instrument}')",
                "print(f'Position: ({x_position}, {y_position})')"
            ],
            challenge='Move at least one band member to the 50-yard line (x=50).'
        )
        
    def validate(self, band_api) -> Tuple[bool, str]:
        """Check if any member is at x=50."""
        for member in band_api.members:
            if abs(member.x - 50) < 1.0:
                return True, "✓ Perfect! You've placed a member at the 50-yard line!"
        return False, "❌ Try moving a member to x=50 using band.move_to(member, 50, y)"


class Module1Lesson2(Lesson):
    """Module 1, Lesson 2: Basic Commands & Functions."""
    
    def __init__(self):
        super().__init__(
            id='week1_lesson2',
            title='Form Up! - Basic Commands',
            description='Use functions to move groups of band members into formation.',
            initial_code=[
                "# Lesson 1.2: Basic Commands & Functions",
                "# Challenge: Form a line with the brass section",
                "",
                "# Get all brass members",
                "brass_members = brass",
                "",
                "# Form them into a line from (20,20) to (80,20)",
                "band.form_line(brass_members, 20, 20, 80, 20)",
                "",
                "print(f'Brass section formed with {len(brass_members)} members')"
            ],
            challenge='Use band.form_line() to create a formation with the brass section.'
        )
        
    def validate(self, band_api) -> Tuple[bool, str]:
        """Check if brass members form a line."""
        brass = band_api.get_section('brass')
        if not brass:
            return False, "❌ No brass members found."
            
        # Check if they're roughly aligned (y-coordinates similar)
        y_coords = [m.y for m in brass]
        if len(set([round(y) for y in y_coords])) <= 2:  # Roughly same y
            return True, "✓ Great! The brass section is in formation!"
        return False, "❌ Use band.form_line(brass, x1, y1, x2, y2) to align them."


class Module1Lesson3(Lesson):
    """Module 1, Lesson 3: Operators & Expressions."""
    
    def __init__(self):
        super().__init__(
            id='week1_lesson3',
            title='On the Count - Operators',
            description='Use arithmetic to calculate precise positions.',
            initial_code=[
                "# Lesson 1.3: Operators & Expressions",
                "# Challenge: Calculate the midpoint between two positions",
                "",
                "# Starting positions",
                "left_position = 20",
                "right_position = 80",
                "",
                "# Calculate the middle using arithmetic",
                "middle = (left_position + right_position) / 2",
                "",
                "# Move a member to the middle",
                "member = members[0]",
                "band.move_to(member, middle, 26)",
                "",
                "print(f'Middle position: {middle}')"
            ],
            challenge='Calculate and move a member to the exact center of the field (x=50, y=26.67).'
        )
        
    def validate(self, band_api) -> Tuple[bool, str]:
        """Check if a member is at the center."""
        for member in band_api.members:
            if abs(member.x - 50) < 2 and abs(member.y - 26.67) < 2:
                return True, "✓ Excellent! You found the exact center!"
        return False, "❌ Calculate the center: x=50, y=26.67"


class LessonManager:
    """Manages all lessons and curriculum."""
    
    def __init__(self):
        self.lessons: Dict[str, Lesson] = {}
        self._initialize_lessons()
        
    def _initialize_lessons(self):
        """Load all lessons into the manager."""
        # Module 1
        self.lessons['week1_lesson1'] = Module1Lesson1()
        self.lessons['week1_lesson2'] = Module1Lesson2()
        self.lessons['week1_lesson3'] = Module1Lesson3()
        
        # TODO: Add more modules
        
    def get_lesson(self, lesson_id: str) -> Lesson:
        """Get a lesson by ID."""
        return self.lessons.get(lesson_id)
        
    def get_all_lessons(self) -> List[Lesson]:
        """Get all available lessons."""
        return list(self.lessons.values())
        
    def validate_lesson(self, lesson_id: str, band_api) -> Tuple[bool, str]:
        """Validate a lesson's completion."""
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return False, "Lesson not found."
        return lesson.validate(band_api)
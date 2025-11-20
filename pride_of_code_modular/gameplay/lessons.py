"""
Lessons - Curriculum implementation for Code of Pride.

This module implements the complete curriculum with lessons for each module
of the "Code of Pride" educational program.
"""

import pygame
from typing import List, Dict, Optional


class LessonManager:
    """Manages the curriculum lessons."""
    
    def __init__(self):
        self.modules = self._create_curriculum()
        
    def _create_curriculum(self) -> List[Dict]:
        """Create the complete curriculum.
        
        Returns:
            List of module dictionaries
        """
        curriculum = [
            {
                'module': 1,
                'title': 'First Rehearsal',
                'description': 'Learn Python basics through marching band fundamentals',
                'lessons': [
                    {
                        'lesson': 1,
                        'title': 'Meet the Band',
                        'concept': 'Variables & Data Types (integers, strings, floats)',
                        'challenge': 'Assign a specific instrument (string) and a position (integer pair) to a single band member.',
                        'expected_code': [
                            '# Create a band member',
                            'member = band.get_member(0)',
                            '# Assign instrument',
                            'member.instrument = "trumpet"',
                            '# Assign position',
                            'member.x = 20',
                            'member.y = 30'
                        ],
                        'hints': [
                            'Use band.get_member(0) to get the first band member',
                            'Assign strings using quotes: "trumpet"',
                            'Assign numbers directly: member.x = 20'
                        ],
                        'expected_lines': 6,
                        'time_estimate': 5  # minutes
                    },
                    {
                        'lesson': 2,
                        'title': 'Form Up!',
                        'concept': 'Basic Commands & Functions (move_to(x, y), turn(direction))',
                        'challenge': 'Use pre-defined functions to move a small group of three band members into a simple line formation.',
                        'expected_code': [
                            '# Get three members',
                            'members = band.get_all_members()[:3]',
                            '# Move to positions',
                            'band.move_to(members[0], 20, 25)',
                            'band.move_to(members[1], 25, 25)',
                            'band.move_to(members[2], 30, 25)'
                        ],
                        'hints': [
                            'Use band.get_all_members() to get all members',
                            'Use list slicing [0:3] to get the first three',
                            'Use band.move_to(member, x, y) to move members'
                        ],
                        'expected_lines': 6,
                        'time_estimate': 7
                    },
                    {
                        'lesson': 3,
                        'title': 'On the Count',
                        'concept': 'Operators & Expressions (+, -, *, /)',
                        'challenge': 'Calculate the coordinates needed to place a band member exactly in the center of two others using arithmetic operators.',
                        'expected_code': [
                            '# Get two members',
                            'member1 = band.get_member(0)',
                            'member2 = band.get_member(1)',
                            '# Calculate center position',
                            'center_x = (member1.x + member2.x) / 2',
                            'center_y = (member1.y + member2.y) / 2',
                            '# Place third member at center',
                            'member3 = band.get_member(2)',
                            'band.move_to(member3, center_x, center_y)'
                        ],
                        'hints': [
                            'Add coordinates and divide by 2 to find center',
                            'Use parentheses to ensure correct order of operations',
                            'Remember that division uses / in Python'
                        ],
                        'expected_lines': 8,
                        'time_estimate': 10
                    }
                ]
            },
            {
                'module': 2,
                'title': 'Learning the Drill',
                'description': 'Master control flow with marching band movements',
                'lessons': [
                    {
                        'lesson': 1,
                        'title': 'If the Drum Major Says...',
                        'concept': 'Conditional Statements (if, elif, else)',
                        'challenge': 'Write a script where the band forms a different shape depending on the value of a variable (e.g., if song_part is "verse," form a block; if it\'s "chorus," form a circle).',
                        'expected_code': [
                            '# Define song part',
                            'song_part = "verse"',
                            '# Form different shapes based on song part',
                            'if song_part == "verse":',
                            '    # Form a block with brass section',
                            '    brass = band.get_section("brass")',
                            '    band.form_block(brass, 20, 20, 2)',
                            'elif song_part == "chorus":',
                            '    # Form a circle with all members',
                            '    members = band.get_all_members()',
                            '    band.form_circle(members, 50, 26, 10)',
                            'else:',
                            '    # Form a line as default',
                            '    members = band.get_all_members()',
                            '    band.form_line(members, 20, 26, 80, 26)'
                        ],
                        'hints': [
                            'Use == to compare strings',
                            'Remember to use colons : after if, elif, and else',
                            'Indent the code inside each condition'
                        ],
                        'expected_lines': 14,
                        'time_estimate': 12
                    },
                    {
                        'lesson': 2,
                        'title': 'Repeat the Phrase',
                        'concept': 'Loops (for, while)',
                        'challenge': 'Instead of writing the move_forward() command eight times, use a for loop to make the entire band march forward eight steps.',
                        'expected_code': [
                            '# Get all band members',
                            'members = band.get_all_members()',
                            '# March forward 8 steps',
                            'for step in range(8):',
                            '    for member in members:',
                            '        band.move_forward(member, 1)'
                        ],
                        'hints': [
                            'Use range(8) to repeat 8 times',
                            'Use nested loops: one for steps, one for members',
                            'Remember to indent code inside loops'
                        ],
                        'expected_lines': 6,
                        'time_estimate': 10
                    },
                    {
                        'lesson': 3,
                        'title': 'Breaking Formation',
                        'concept': 'Loop Control (break, continue)',
                        'challenge': 'Create a drill where the color guard spins their flags in a loop, but uses a break command to stop spinning and hold a pose on a specific musical cue.',
                        'expected_code': [
                            '# Get color guard members',
                            'guard = band.get_section("guard")',
                            '# Spin flags for 10 beats or until cue',
                            'for beat in range(10):',
                            '    # Check for musical cue (simulated)',
                            '    if beat == 7:',  # On beat 7, stop spinning
                            '        break',
                            '    # Spin flags',
                            '    for member in guard:',
                            '        member.facing = (member.facing + 45) % 360'
                        ],
                        'hints': [
                            'Use break to exit a loop early',
                            'Use continue to skip to the next iteration',
                            'Angles are measured in degrees (0-359)'
                        ],
                        'expected_lines': 10,
                        'time_estimate': 15
                    }
                ]
            },
            {
                'module': 3,
                'title': 'Section Leaders',
                'description': 'Organize and manage data structures with band sections',
                'lessons': [
                    {
                        'lesson': 1,
                        'title': 'The Roster',
                        'concept': 'Lists & List Methods (append, remove, indexing)',
                        'challenge': 'Create a list of all the brass players and then write a loop to move them as a single unit.',
                        'expected_code': [
                            '# Create a list of brass players',
                            'brass_players = band.get_section("brass")',
                            '# Move all brass players together',
                            'for player in brass_players:',
                            '    band.move_to(player, player.x + 10, player.y)'
                        ],
                        'hints': [
                            'Use band.get_section("section_name") to get section members',
                            'Use for loops to iterate through lists',
                            'Access list elements with indexing: list[index]'
                        ],
                        'expected_lines': 5,
                        'time_estimate': 8
                    },
                    {
                        'lesson': 2,
                        'title': 'The Drill Book',
                        'concept': 'Dictionaries',
                        'challenge': 'Create a dictionary where each key is a section name (e.g., "brass") and the value is a list of its members\' coordinates. Use this to command sections by name.',
                        'expected_code': [
                            '# Create a drill book with section coordinates',
                            'drill_book = {}',
                            'sections = ["brass", "woodwind", "percussion", "guard"]',
                            'for section_name in sections:',
                            '    section_members = band.get_section(section_name)',
                            '    drill_book[section_name] = [(m.x, m.y) for m in section_members]',
                            '# Command a specific section',
                            'brass_coords = drill_book["brass"]'
                        ],
                        'hints': [
                            'Create dictionaries with curly braces: {}',
                            'Use keys to access values: dictionary[key]',
                            'Use list comprehensions to create lists: [expression for item in list]'
                        ],
                        'expected_lines': 8,
                        'time_estimate': 12
                    },
                    {
                        'lesson': 3,
                        'title': 'Uniform Check',
                        'concept': 'Tuples & Sets',
                        'challenge': 'Use a tuple to store the fixed (x, y) coordinates for a set of "dots" on the field. Use a set to ensure a list of band members is unique before assigning them to a formation.',
                        'expected_code': [
                            '# Define fixed dot positions as tuples',
                            'dot_positions = [(20, 20), (50, 26), (80, 20)]',
                            '# Create a set of unique member IDs',
                            'member_ids = band.get_all_members()',
                            'unique_ids = set([m.id for m in member_ids])',
                            '# Place members at dot positions',
                            'for i, (x, y) in enumerate(dot_positions):',
                            '    if i < len(member_ids):',
                            '        band.move_to(member_ids[i], x, y)'
                        ],
                        'hints': [
                            'Tuples are created with parentheses: (x, y)',
                            'Sets are created with curly braces: {1, 2, 3}',
                            'Sets automatically remove duplicates'
                        ],
                        'expected_lines': 9,
                        'time_estimate': 10
                    }
                ]
            },
            {
                'module': 4,
                'title': 'Advanced Choreography',
                'description': 'Create reusable and modular code for complex formations',
                'lessons': [
                    {
                        'lesson': 1,
                        'title': 'Writing a New Move',
                        'concept': 'Defining Functions (def)',
                        'challenge': 'Create a custom function called form_circle(center_x, center_y, radius) that takes coordinates and a size and makes any given list of band members form a perfect circle.',
                        'expected_code': [
                            '# Define a custom function to form a circle',
                            'def form_circle(members, center_x, center_y, radius):',
                            '    import math',
                            '    count = len(members)',
                            '    for i, member in enumerate(members):',
                            '        angle = (2 * math.pi * i) / count',
                            '        x = center_x + radius * math.cos(angle)',
                            '        y = center_y + radius * math.sin(angle)',
                            '        band.move_to(member, x, y)',
                            '# Use the function',
                            'members = band.get_all_members()',
                            'form_circle(members, 50, 26, 15)'
                        ],
                        'hints': [
                            'Use def to define functions',
                            'Use import inside functions when needed',
                            'Remember to indent function code',
                            'Call functions by name: function_name(arguments)'
                        ],
                        'expected_lines': 11,
                        'time_estimate': 15
                    },
                    {
                        'lesson': 2,
                        'title': 'The Drill Library',
                        'concept': 'Importing Modules',
                        'challenge': 'The game provides a new module called advanced_moves. The player must import it and use its pre-built functions, like scatter_formation() or company_front().',
                        'expected_code': [
                            '# Import the advanced moves module',
                            'import advanced_moves',
                            '# Use a pre-built function',
                            'members = band.get_all_members()',
                            'advanced_moves.scatter_formation(members, 20, 20, 80, 40)',
                            '# Use another pre-built function',
                            'advanced_moves.company_front(members, 50, 26)'
                        ],
                        'hints': [
                            'Use import module_name to import modules',
                            'Use module_name.function_name() to call functions',
                            'Check documentation for function parameters'
                        ],
                        'expected_lines': 6,
                        'time_estimate': 8
                    },
                    {
                        'lesson': 3,
                        'title': 'Perfecting the Technique',
                        'concept': 'Function Arguments & Scope',
                        'challenge': 'Refine the form_circle function by adding arguments for the number of performers and the starting angle, learning about default arguments and variable scope.',
                        'expected_code': [
                            '# Enhanced form_circle function with default arguments',
                            'def form_circle(members, center_x, center_y, radius, start_angle=0):',
                            '    import math',
                            '    count = len(members)',
                            '    for i, member in enumerate(members):',
                            '        angle = start_angle + (2 * math.pi * i) / count',
                            '        x = center_x + radius * math.cos(angle)',
                            '        y = center_y + radius * math.sin(angle)',
                            '        band.move_to(member, x, y)',
                            '# Use with default argument',
                            'members = band.get_all_members()',
                            'form_circle(members, 50, 26, 15)',
                            '# Use with custom starting angle',
                            'form_circle(members, 50, 26, 15, math.pi/2)'
                        ],
                        'hints': [
                            'Set default values with argument=default',
                            'Variables inside functions are local scope',
                            'Import statements inside functions only affect that function'
                        ],
                        'expected_lines': 13,
                        'time_estimate': 15
                    }
                ]
            },
            {
                'module': 5,
                'title': 'The Championship Show',
                'description': 'Master Object-Oriented Programming with complex performers',
                'lessons': [
                    {
                        'lesson': 1,
                        'title': 'Defining the Performer',
                        'concept': 'Classes & Objects',
                        'challenge': 'Create a Performer class with attributes like instrument, position, and section, and methods like march() and turn().',
                        'expected_code': [
                            '# Define a Performer class',
                            'class Performer:',
                            '    def __init__(self, instrument, x, y, section):',
                            '        self.instrument = instrument',
                            '        self.x = x',
                            '        self.y = y',
                            '        self.section = section',
                            '        self.facing = 0',
                            '    ',
                            '    def march(self, steps):',
                            '        import math',
                            '        radians = math.radians(self.facing)',
                            '        self.x += math.sin(radians) * steps',
                            '        self.y += math.cos(radians) * steps',
                            '    ',
                            '    def turn(self, degrees):',
                            '        self.facing = (self.facing + degrees) % 360',
                            '# Create performer instances',
                            'performer1 = Performer("trumpet", 20, 20, "brass")',
                            'performer2 = Performer("trombone", 25, 20, "brass")'
                        ],
                        'hints': [
                            'Use class to define classes',
                            'Use __init__ for initialization',
                            'Use self to refer to instance attributes',
                            'Methods are functions defined inside classes'
                        ],
                        'expected_lines': 20,
                        'time_estimate': 20
                    },
                    {
                        'lesson': 2,
                        'title': 'Instrument Sections',
                        'concept': 'Inheritance',
                        'challenge': 'Create subclasses of Performer, such as BrassPlayer and ColorGuard, which inherit from the parent class but have their own unique methods (e.g., ColorGuard.spin_flag()).',
                        'expected_code': [
                            '# Parent class',
                            'class Performer:',
                            '    def __init__(self, instrument, x, y, section):',
                            '        self.instrument = instrument',
                            '        self.x = x',
                            '        self.y = y',
                            '        self.section = section',
                            '    ',
                            '# Brass player subclass',
                            'class BrassPlayer(Performer):',
                            '    def __init__(self, instrument, x, y):',
                            '        super().__init__(instrument, x, y, "brass")',
                            '    ',
                            '    def play_fanfare(self):',
                            '        return "TOOT TOOT!"',
                            '# Color guard subclass',
                            'class ColorGuard(Performer):',
                            '    def __init__(self, prop, x, y):',
                            '        super().__init__(prop, x, y, "guard")',
                            '        self.prop = prop',
                            '    ',
                            '    def spin_flag(self):',
                            '        self.facing = (self.facing + 180) % 360',
                            '# Create instances',
                            'trumpeter = BrassPlayer("trumpet", 20, 20)',
                            'flag_spinner = ColorGuard("flag", 30, 20)'
                        ],
                        'hints': [
                            'Use class Child(Parent) to create subclasses',
                            'Use super() to call parent class methods',
                            'Subclasses inherit all parent attributes and methods',
                            'Subclasses can add new attributes and methods'
                        ],
                        'expected_lines': 25,
                        'time_estimate': 25
                    },
                    {
                        'lesson': 3,
                        'title': 'The Full Ensemble',
                        'concept': 'Polymorphism',
                        'challenge': 'Create a list of Performer objects of different types. Use a loop to call a common method like perform() on each object, demonstrating how each subclass implements the method differently.',
                        'expected_code': [
                            '# Parent class with common method',
                            'class Performer:',
                            '    def __init__(self, instrument, x, y, section):',
                            '        self.instrument = instrument',
                            '        self.x = x',
                            '        self.y = y',
                            '        self.section = section',
                            '    ',
                            '    def perform(self):',
                            '        return f"{self.instrument} plays music"',
                            '# Brass player subclass',
                            'class BrassPlayer(Performer):',
                            '    def perform(self):',
                            '        return f"{self.instrument} plays a fanfare"',
                            '# Color guard subclass',
                            'class ColorGuard(Performer):',
                            '    def perform(self):',
                            '        return f"{self.instrument} spins gracefully"',
                            '# Create ensemble of different performers',
                            'ensemble = [',
                            '    BrassPlayer("trumpet", 20, 20),',
                            '    BrassPlayer("trombone", 25, 20),',
                            '    ColorGuard("flag", 30, 20),',
                            '    ColorGuard("rifle", 35, 20)',
                            ']',
                            '# Call perform method on all performers',
                            'for performer in ensemble:',
                            '    print(performer.perform())'
                        ],
                        'hints': [
                            'Polymorphism allows different classes to be treated the same way',
                            'Methods with the same name can behave differently in subclasses',
                            'Use loops to call the same method on different object types',
                            'The correct method is automatically selected based on the object type'
                        ],
                        'expected_lines': 28,
                        'time_estimate': 25
                    }
                ]
            }
        ]
        
        return curriculum
        
    def get_module(self, module_num: int) -> Optional[Dict]:
        """Get a module by number.
        
        Args:
            module_num: Module number (1-5)
            
        Returns:
            Module dictionary or None if not found
        """
        for module in self.modules:
            if module['module'] == module_num:
                return module
        return None
        
    def get_lesson(self, module_num: int, lesson_num: int) -> Optional[Dict]:
        """Get a specific lesson.
        
        Args:
            module_num: Module number (1-5)
            lesson_num: Lesson number (1-3)
            
        Returns:
            Lesson dictionary or None if not found
        """
        module = self.get_module(module_num)
        if not module:
            return None
            
        for lesson in module['lessons']:
            if lesson['lesson'] == lesson_num:
                return lesson
        return None
        
    def get_all_modules(self) -> List[Dict]:
        """Get all modules.
        
        Returns:
            List of all module dictionaries
        """
        return self.modules.copy()
        
    def get_module_lessons(self, module_num: int) -> List[Dict]:
        """Get all lessons for a module.
        
        Args:
            module_num: Module number (1-5)
            
        Returns:
            List of lesson dictionaries
        """
        module = self.get_module(module_num)
        if not module:
            return []
        return module['lessons'].copy()
        
    def get_progress_stats(self, completed_lessons: set) -> Dict:
        """Get curriculum progress statistics.
        
        Args:
            completed_lessons: Set of (module, lesson) tuples that are completed
            
        Returns:
            Dictionary with progress statistics
        """
        total_lessons = 0
        completed_count = 0
        
        for module in self.modules:
            module_num = module['module']
            for lesson in module['lessons']:
                lesson_num = lesson['lesson']
                total_lessons += 1
                if (module_num, lesson_num) in completed_lessons:
                    completed_count += 1
                    
        return {
            'total_lessons': total_lessons,
            'completed_lessons': completed_count,
            'completion_percentage': (completed_count / max(1, total_lessons)) * 100
        }
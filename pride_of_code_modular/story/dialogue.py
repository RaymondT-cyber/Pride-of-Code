"""
Dialogue System - Narrative voice-overs for Code of Pride.

This module implements the dialogue system for character interactions
and narrative voice-overs.
"""

import pygame
import random
from typing import List, Dict, Optional


class DialogueSystem:
    """Manages character dialogue and narrative voice-overs."""
    
    def __init__(self):
        self.characters = {
            'drum_major': {
                'name': 'Drum Major Maya',
                'voice_traits': {
                    'tone': 'confident',
                    'pace': 'moderate',
                    'style': 'encouraging'
                },
                'dialogue_variants': {
                    'encouragement': [
                        "Great job! You're getting the hang of this!",
                        "That's exactly right! Keep up the excellent work!",
                        "I can see you're putting in real effort. Well done!",
                        "Perfect formation! You're a natural at this!"
                    ],
                    'hints': [
                        "Remember to check your syntax carefully.",
                        "Try breaking the problem into smaller steps.",
                        "Think about how you can use loops to simplify your code.",
                        "Don't forget to test your code before running it!"
                    ],
                    'challenge': [
                        "This next drill is going to be tricky, but I know you can handle it!",
                        "Let's see what you've learned with this more complex challenge.",
                        "Time to put your skills to the test with a real challenge!",
                        "This formation requires precision. Take your time and think it through."
                    ]
                }
            },
            'band_director': {
                'name': 'Mr. Rodriguez',
                'voice_traits': {
                    'tone': 'authoritative',
                    'pace': 'slow',
                    'style': 'instructional'
                },
                'dialogue_variants': {
                    'briefing': [
                        "Welcome to today's rehearsal. Here's what we need to accomplish.",
                        "Today's challenge will test everything you've learned so far.",
                        "This week's performance is critical. Let's make it count.",
                        "I've designed this drill to push your programming skills to the limit."
                    ],
                    'feedback': [
                        "Precision is everything in both music and code.",
                        "Every line of code is like a note in our performance.",
                        "Attention to detail separates good programmers from great ones.",
                        "Your code should be as clean and precise as our marching formations."
                    ],
                    'conclusion': [
                        "Excellent work today. This is exactly the quality I expect.",
                        "That performance was outstanding. You're ready for the competition.",
                        "Perfect execution! This is what I like to see.",
                        "You've mastered today's lesson. Well done, everyone."
                    ]
                }
            },
            'brass_leader': {
                'name': 'Brass Section Leader',
                'voice_traits': {
                    'tone': 'enthusiastic',
                    'pace': 'fast',
                    'style': 'supportive'
                },
                'dialogue_variants': {
                    'greeting': [
                        "Hey there! Ready to brass it up?",
                        "Let's make some noise with our code!",
                        "Brass players unite! Let's code some formations!",
                        "Time to show them what brass can do!"
                    ],
                    'tips': [
                        "Brass players always hit the right note - just like your code should!",
                        "In brass, we blow our horns loud - make your code stand out!",
                        "Every brass player knows timing is key - just like in programming!",
                        "Brass sections work as a team - just like your code functions!"
                    ]
                }
            },
            'woodwind_leader': {
                'name': 'Woodwind Section Leader',
                'voice_traits': {
                    'tone': 'gentle',
                    'pace': 'moderate',
                    'style': 'thoughtful'
                },
                'dialogue_variants': {
                    'greeting': [
                        "Hello! Let's create something beautiful together.",
                        "Woodwinds bring harmony to music, just like clean code brings harmony to programs.",
                        "Let's approach this challenge with precision and grace.",
                        "Ready to weave some elegant code patterns?"
                    ],
                    'tips': [
                        "Like a woodwind instrument, your code should flow smoothly.",
                        "Woodwinds require careful breath control - your code needs careful logic control.",
                        "Each woodwind has its unique voice - each function should have a unique purpose.",
                        "Harmony in music comes from each instrument playing its part - harmony in code comes from each function doing its job."
                    ]
                }
            },
            'percussion_leader': {
                'name': 'Percussion Section Leader',
                'voice_traits': {
                    'tone': 'energetic',
                    'pace': 'fast',
                    'style': 'rhythmic'
                },
                'dialogue_variants': {
                    'greeting': [
                        "Let's beat this challenge into submission!",
                        "Time to drum up some awesome code!",
                        "Percussion power! Let's code with rhythm!",
                        "Get ready to rock... I mean, code!"
                    ],
                    'tips': [
                        "In percussion, timing is everything - in programming, logic is everything!",
                        "Every beat counts in percussion - every line counts in code!",
                        "Percussion keeps the rhythm - your code should keep the logical flow!",
                        "We hit hard in percussion - make your code hit hard with efficiency!"
                    ]
                }
            },
            'guard_leader': {
                'name': 'Color Guard Leader',
                'voice_traits': {
                    'tone': 'graceful',
                    'pace': 'moderate',
                    'style': 'artistic'
                },
                'dialogue_variants': {
                    'greeting': [
                        "Let's paint the field with beautiful code!",
                        "Time to add some flair to our programming!",
                        "Color Guard style - let's make our code visually stunning!",
                        "Ready to choreograph some elegant algorithms?"
                    ],
                    'tips': [
                        "Like a flag routine, your code should be graceful and purposeful.",
                        "Every spin in color guard has meaning - every function in your code should have purpose.",
                        "We create visual art with our movements - you can create logical art with your code.",
                        "Precision in our spins leads to beauty - precision in your code leads to functionality."
                    ]
                }
            }
        }
        
        # Current dialogue state
        self.current_dialogue = None
        self.dialogue_index = 0
        self.dialogue_complete = False
        
        # Font setup
        self.font = pygame.font.SysFont('arial', 16)
        self.name_font = pygame.font.SysFont('arial', 18, bold=True)
        
        # Colors
        self.colors = {
            'background': (30, 30, 40, 220),  # Semi-transparent
            'border': (46, 94, 170),  # Blue
            'text': (240, 240, 240),
            'name': (255, 184, 28)  # Gold
        }
        
    def get_character_dialogue(self, character: str, dialogue_type: str) -> str:
        """Get a random dialogue line for a character.
        
        Args:
            character: Character name
            dialogue_type: Type of dialogue (encouragement, hints, etc.)
            
        Returns:
            Dialogue line
        """
        if character not in self.characters:
            return "..."
            
        char_data = self.characters[character]
        if dialogue_type not in char_data['dialogue_variants']:
            # Return any dialogue if specific type not found
            all_dialogue = []
            for lines in char_data['dialogue_variants'].values():
                all_dialogue.extend(lines)
            return random.choice(all_dialogue) if all_dialogue else "..."
            
        return random.choice(char_data['dialogue_variants'][dialogue_type])
        
    def start_dialogue_sequence(self, character: str, dialogue_sequence: List[str]):
        """Start a sequence of dialogue lines.
        
        Args:
            character: Character speaking
            dialogue_sequence: List of dialogue lines
        """
        if not dialogue_sequence:
            self.current_dialogue = None
            self.dialogue_complete = True
            return
            
        self.current_dialogue = {
            'character': character,
            'name': self.characters.get(character, {}).get('name', character),
            'sequence': dialogue_sequence,
            'current_index': 0
        }
        self.dialogue_complete = False
        
    def advance_dialogue(self) -> bool:
        """Advance to the next line in the dialogue sequence.
        
        Returns:
            True if there's more dialogue, False if sequence is complete
        """
        if not self.current_dialogue:
            self.dialogue_complete = True
            return False
            
        self.current_dialogue['current_index'] += 1
        
        if self.current_dialogue['current_index'] >= len(self.current_dialogue['sequence']):
            self.current_dialogue = None
            self.dialogue_complete = True
            return False
            
        return True
        
    def get_current_dialogue(self) -> Optional[Dict]:
        """Get the current dialogue information.
        
        Returns:
            Dictionary with current dialogue information or None
        """
        if not self.current_dialogue:
            return None
            
        return {
            'character': self.current_dialogue['character'],
            'name': self.current_dialogue['name'],
            'line': self.current_dialogue['sequence'][self.current_dialogue['current_index']],
            'index': self.current_dialogue['current_index'],
            'total': len(self.current_dialogue['sequence'])
        }
        
    def is_dialogue_complete(self) -> bool:
        """Check if the current dialogue sequence is complete.
        
        Returns:
            True if dialogue is complete, False otherwise
        """
        return self.dialogue_complete
        
    def draw_dialogue_box(self, surface: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw the current dialogue in a box.
        
        Args:
            surface: Surface to draw on
            x, y: Position of the dialogue box
            width, height: Dimensions of the dialogue box
        """
        if not self.current_dialogue:
            return
            
        # Draw background
        bg_rect = pygame.Rect(x, y, width, height)
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill(self.colors['background'])
        surface.blit(s, (x, y))
        pygame.draw.rect(surface, self.colors['border'], bg_rect, 2)
        
        # Get current dialogue
        dialogue = self.get_current_dialogue()
        if not dialogue:
            return
            
        # Draw character name
        name_surf = self.name_font.render(dialogue['name'], True, self.colors['name'])
        surface.blit(name_surf, (x + 10, y + 10))
        
        # Draw dialogue line
        line_surf = self.font.render(dialogue['line'], True, self.colors['text'])
        surface.blit(line_surf, (x + 10, y + 40))
        
        # Draw progress indicator
        progress = f"{dialogue['index'] + 1}/{dialogue['total']}"
        progress_surf = self.font.render(progress, True, (150, 150, 150))
        surface.blit(progress_surf, (x + width - 50, y + height - 25))
        
        # Draw continue prompt
        prompt = "Press SPACE to continue..."
        prompt_surf = self.font.render(prompt, True, (200, 200, 200))
        surface.blit(prompt_surf, (x + 10, y + height - 25))
        
    def get_story_beat_dialogue(self, story_beat: str, week: int) -> List[str]:
        """Get dialogue for a specific story beat.
        
        Args:
            story_beat: Current story beat
            week: Current week number
            
        Returns:
            List of dialogue lines
        """
        dialogue_map = {
            'preseason': [
                "Welcome to the Pride of Casa Grande marching band!",
                "I'm Drum Major Maya, and I'll be helping you learn our drill system.",
                "This season, you'll be our new Drill Writer, programming our formations with Python.",
                "Let's start with something simple to get you familiar with the system.",
                "Use the code editor on the left to move band members around the field."
            ],
            'first_game': [
                "Great work during practice! Our first game is this Friday.",
                "Mr. Rodriguez has designed a special routine for our debut performance.",
                "This formation requires precise timing - just like your code needs precise logic.",
                "Remember, in both programming and marching band, attention to detail is crucial.",
                "Let's show the crowd what the Pride of Casa Grande can do!"
            ],
            'rivalry': [
                "This week's game is against our biggest rivals, Desert Ridge.",
                "The pressure is on, but I know we can rise to the challenge.",
                "This formation is more complex than anything we've done before.",
                "You'll need to use everything you've learned about loops and functions.",
                "Let's show them what Casa Grande pride really means!"
            ],
            'homecoming': [
                "Homecoming week is always special. The whole school will be watching.",
                "We've been working on something really special for this performance.",
                "This routine combines all the Python concepts you've learned so far.",
                "It's going to take careful planning and precise execution.",
                "I have complete confidence in your abilities as our Drill Writer."
            ],
            'midseason': [
                "We're halfway through the season, and you're doing an amazing job!",
                "The regionals are coming up, so we need to step up our game.",
                "This week's challenge will test your understanding of data structures.",
                "You'll be organizing our sections using lists and dictionaries.",
                "Remember, a good programmer is like a good section leader - organized and efficient."
            ],
            'playoffs': [
                "We made it to the playoffs! This is what we've been working toward.",
                "The competition will be fierce, but our programming skills give us an edge.",
                "This performance requires advanced techniques - functions and modules.",
                "You've come a long way since preseason. I'm proud of your progress.",
                "Let's show them the power of Python and the Pride of Casa Grande!"
            ],
            'championship': [
                "This is it - the championship game! We've worked so hard to get here.",
                "This final performance needs to be absolutely perfect.",
                "You'll be using all your Python skills - from basics to object-oriented programming.",
                "Every band member is counting on us to give them the best show possible.",
                "This is your moment to shine. Make the Pride of Casa Grande proud!"
            ]
        }
        
        return dialogue_map.get(story_beat, [
            "Another great week of practice!",
            "You're becoming a skilled Drill Writer.",
            "Keep up the excellent work!",
            "Let's continue building on what we've learned."
        ])
        
    def get_character_introduction(self, character: str) -> List[str]:
        """Get introduction dialogue for a character.
        
        Args:
            character: Character name
            
        Returns:
            List of introduction dialogue lines
        """
        introductions = {
            'drum_major': [
                "Hi there! I'm Drum Major Maya, your guide through this marching band adventure.",
                "I'll be helping you learn how to program our formations using Python.",
                "Don't worry if it seems tricky at first - we all start somewhere!",
                "Remember, every expert was once a beginner. You've got this!"
            ],
            'band_director': [
                "Good day. I'm Mr. Rodriguez, director of the Pride of Casa Grande.",
                "As your band director, I'm responsible for our show's artistic vision.",
                "I'll be assigning you challenges that push your programming abilities.",
                "Precision and dedication - these qualities make both great musicians and great programmers."
            ],
            'brass_leader': [
                "Hey! I'm the Brass Section Leader, ready to add some power to our code!",
                "Brass instruments are loud and proud - just like your code should be clear and confident!",
                "We'll be working on formations that really showcase our section.",
                "Let's make some noise with our programming skills!"
            ],
            'woodwind_leader': [
                "Hello, I'm the Woodwind Section Leader.",
                "Woodwinds add harmony and beauty to our music, just as clean code adds elegance to programs.",
                "I'll help you create precise and graceful code solutions.",
                "Let's approach each challenge with thoughtfulness and attention to detail."
            ],
            'percussion_leader': [
                "Rock on! I'm the Percussion Section Leader, bringing the beat to our code!",
                "In percussion, timing is everything - in programming, logic is everything!",
                "We'll be creating routines with rhythm and precision.",
                "Get ready to drum up some amazing code with me!"
            ],
            'guard_leader': [
                "Greetings! I'm the Color Guard Leader, here to add visual flair to our programming!",
                "Just as we create beautiful visual performances, you'll be creating elegant code solutions.",
                "I'll help you make your code as graceful and purposeful as our flag routines.",
                "Let's paint the field of programming with beautiful, functional code!"
            ]
        }
        
        return introductions.get(character, [
            "Hello! I'm excited to work with you this season.",
            "Together, we'll create amazing formations using Python.",
            "Let's make this season unforgettable!"
        ])
# Code of Pride: User Guide

Welcome to "Code of Pride: A Python Marching Band Adventure"! This guide will help you get started with the game and understand all its features.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Game Modes](#game-modes)
4. [The Code Editor](#the-code-editor)
5. [The Marching Field](#the-marching-field)
6. [Curriculum Overview](#curriculum-overview)
7. [Scoring System](#scoring-system)
8. [Tips and Tricks](#tips-and-tricks)
9. [Troubleshooting](#troubleshooting)

## Introduction

"Code of Pride" is an innovative educational game that teaches Python programming through the creative world of high school marching band. You'll write Python code to command a virtual marching band, the "Pride of Casa Grande," to perform intricate drills and formations on a digital football field.

## Getting Started

### System Requirements

- Operating System: Windows 10+, macOS 10.12+, or Ubuntu 16.04+
- Processor: Dual-core 2.0 GHz or better
- Memory: 4 GB RAM minimum
- Graphics: Integrated graphics with OpenGL 3.3 support
- Storage: 500 MB available space

### Installation

1. Download the latest version of Code of Pride from [our website](#)
2. Extract the ZIP file to your preferred location
3. Run the executable file (`code_of_pride.exe` on Windows, `code_of_pride` on macOS/Linux)

### First Launch

When you first launch the game, you'll be greeted by Drum Major Maya who will introduce you to the Pride of Casa Grande and help you get started with your first lesson.

## Game Modes

### Campaign Mode: "The Season"

Follow the Pride of Casa Grande through a full competitive season. Each week introduces new programming concepts and culminates in a performance where you design a drill for that week's game.

**Progression:**
- Preseason Practice
- First Game
- Rivalry Week
- Homecoming Spectacular
- Midseason Review
- Playoff Push
- State Championship

### Challenge Mode: "Drill of the Day"

Daily bite-sized challenges that focus on specific programming concepts. Perfect for reinforcing skills or quick practice sessions.

### Sandbox Mode: "Freeform Practice"

An open-ended environment where you can experiment with band formations without any specific goals. Save and share your creations with others.

## The Code Editor

The code editor is where you'll write Python code to control the marching band. It features:

### Features

- **Syntax Highlighting**: Keywords, strings, comments, and numbers are color-coded
- **Line Numbers**: Easily reference specific lines
- **Breakpoints**: Click in the gutter to set breakpoints for debugging
- **Smart Indentation**: Automatically indents new lines
- **Undo/Redo**: Ctrl+Z and Ctrl+Y for undo/redo
- **Clipboard Support**: Ctrl+C, Ctrl+X, Ctrl+V for copy/cut/paste

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save file |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+C | Copy |
| Ctrl+X | Cut |
| Ctrl+V | Paste |
| Ctrl+A | Select all |
| Ctrl+R | Run code |
| Ctrl+G | Toggle grid |
| Ctrl+C | Toggle coordinates |
| Ctrl+L | Toggle section labels |
| Ctrl+D | Toggle score details |

### Band API Reference

The game provides a simple API for controlling band members:

```python
# Get band members
member = band.get_member(0)  # Get member by ID
members = band.get_all_members()  # Get all members
brass = band.get_section('brass')  # Get specific section

# Move members
band.move_to(member, x, y)  # Move to specific position
band.move_forward(member, steps)  # Move forward/backward
band.turn(member, direction)  # Turn member

# Formations
band.form_line(members, start_x, start_y, end_x, end_y)
band.form_circle(members, center_x, center_y, radius)
band.form_block(members, x, y, rows, spacing=5.0)

# Member properties
member.x  # X position (0-100 yards)
member.y  # Y position (0-53.33 yards)
member.section  # Section ('brass', 'woodwind', 'percussion', 'guard')
member.instrument  # Instrument type
member.facing  # Direction (0-359 degrees)
```

## The Marching Field

The marching field simulator shows the results of your code in real-time.

### Field Controls

- **Grid Toggle**: Ctrl+G to show/hide the coordinate grid
- **Coordinates Toggle**: Ctrl+C to show/hide member coordinates
- **Labels Toggle**: Ctrl+L to show/hide section labels
- **Mouse Interaction**: Click on members to select them

### Field Dimensions

- **Length**: 100 yards (0-100)
- **Width**: 53.33 yards (0-53.33)
- **Yard Lines**: Every 5 yards
- **Hash Marks**: At 13.33, 26.67, and 40.0 yard lines

## Curriculum Overview

The game teaches Python through 5 modules with 3 lessons each:

### Module 1: First Rehearsal (Python Basics)
1. Meet the Band - Variables & Data Types
2. Form Up! - Basic Commands & Functions
3. On the Count - Operators & Expressions

### Module 2: Learning the Drill (Control Flow)
1. If the Drum Major Says... - Conditional Statements
2. Repeat the Phrase - Loops
3. Breaking Formation - Loop Control

### Module 3: Section Leaders (Data Structures)
1. The Roster - Lists & List Methods
2. The Drill Book - Dictionaries
3. Uniform Check - Tuples & Sets

### Module 4: Advanced Choreography (Functions & Modules)
1. Writing a New Move - Defining Functions
2. The Drill Library - Importing Modules
3. Perfecting the Technique - Function Arguments & Scope

### Module 5: The Championship Show (Object-Oriented Programming)
1. Defining the Performer - Classes & Objects
2. Instrument Sections - Inheritance
3. The Full Ensemble - Polymorphism

## Scoring System

Earn "Pride Points" by completing challenges successfully:

### Point Categories

- **Correct Formation**: Base points for successful execution
- **Efficient Code**: Bonus for using fewer lines or advanced techniques
- **Creativity**: Points for unique solutions
- **Speed Bonus**: Bonus for completing challenges quickly
- **Streak Bonus**: Increasing multiplier for consecutive successes

### Multiplier System

- Complete challenges successfully to build a streak
- Streaks increase your point multiplier (up to 50% bonus)
- Errors reset your streak

## Tips and Tricks

### General Tips

1. **Start Simple**: Begin with basic movements before attempting complex formations
2. **Test Often**: Run your code frequently to catch errors early
3. **Use Comments**: Add comments to explain complex sections of code
4. **Save Your Work**: Use Sandbox Mode to save interesting formations

### Programming Tips

1. **Variables**: Use variables to store positions and reuse values
2. **Loops**: Use loops to avoid repetitive code
3. **Functions**: Create functions for complex movements you use multiple times
4. **Debugging**: Use print statements to check variable values

### Formation Tips

1. **Spacing**: Keep adequate spacing between band members
2. **Symmetry**: Symmetrical formations are often more visually appealing
3. **Flow**: Consider how formations transition from one to another
4. **Precision**: Exact coordinates create clean, professional-looking formations

## Troubleshooting

### Common Issues

**"Syntax Error" Messages**
- Check for missing colons at the end of if/for/while statements
- Ensure parentheses and brackets are properly closed
- Verify indentation is consistent

**"Name Error" Messages**
- Check that all variable names are spelled correctly
- Ensure variables are defined before use
- Verify that you're using the correct band API methods

**Performance Issues**
- Close other applications to free up system resources
- Reduce the number of band members in Sandbox Mode
- Restart the game if it becomes unresponsive

### Getting Help

- **In-Game Help**: Press F1 to access the help menu
- **Online Documentation**: Visit [our website](#) for complete documentation
- **Community Forum**: Connect with other players at [our forum](#)
- **Support**: Contact support at support@codeofpride.com

## Glossary

- **Band Member**: A virtual performer in the marching band
- **Section**: A group of similar instruments (brass, woodwind, percussion, guard)
- **Formation**: The arrangement of band members on the field
- **Drill**: A sequence of formations performed to music
- **Pride Points**: The game's scoring system

## Credits

"Code of Pride" was created by a team of educators, programmers, and marching band enthusiasts who believe that learning to code should be engaging, creative, and fun.

**Lead Developer**: [Name]
**Educational Design**: [Name]
**Art & Animation**: [Name]
**Sound Design**: [Name]
**Marching Band Consultant**: [Name]

## Version Information

**Current Version**: 1.0.0
**Release Date**: [Date]
**Last Updated**: [Date]

Thank you for choosing Code of Pride! We hope you enjoy learning Python through the exciting world of marching band.
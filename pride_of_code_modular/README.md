# Code of Pride: A Python Marching Band Adventure

"Code of Pride" is an innovative educational game that teaches Python programming through the creative world of high school marching band. Players write Python code to command a virtual marching band, the "Pride of Casa Grande," to perform intricate drills and formations on a digital football field.

## Features

- **Educational Gameplay**: Learn Python programming concepts through hands-on marching band simulations
- **Three Game Modes**: 
  - Campaign Mode: Story-driven season with progressive challenges
  - Challenge Mode: Daily coding challenges
  - Sandbox Mode: Freeform practice environment
- **Comprehensive Curriculum**: 5 modules covering Python basics to object-oriented programming
- **Visual Feedback**: Real-time visualization of code execution on a football field
- **Scoring System**: "Pride Points" to track progress and encourage efficient coding
- **Retro Aesthetics**: 8-bit pixel art style inspired by classic sports games

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Pygame library
- Basic understanding of programming concepts (helpful but not required)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-of-pride.git
   ```

2. Navigate to the project directory:
   ```bash
   cd code-of-pride
   ```

3. Install required dependencies:
   ```bash
   pip install pygame
   ```

4. Run the game:
   ```bash
   python3 core/main.py
   ```

### System Requirements

- **Operating System**: Windows 10+, macOS 10.12+, or Ubuntu 16.04+
- **Processor**: Dual-core 2.0 GHz or better
- **Memory**: 4 GB RAM minimum
- **Graphics**: Integrated graphics with OpenGL 3.3 support
- **Storage**: 500 MB available space

## Project Structure

```
code-of-pride/
├── assets/              # Game assets (images, sounds)
├── core/                # Core game engine files
├── docs/                # Documentation
├── gameplay/            # Game logic and mechanics
├── scenes/              # Game scenes and UI
├── story/               # Narrative content
├── tests/               # Unit tests
├── ui/                  # User interface components
├── config.py            # Game configuration
├── run_tests.py         # Test runner
└── README.md            # This file
```

## Development

### Architecture

The game is built using Python and Pygame with a modular architecture:

- **Core**: Main game loop and system management
- **Gameplay**: Band API, code execution, scoring, and curriculum
- **UI**: Editor, field view, timeline, and menus
- **Story**: Narrative engine and dialogue system
- **Assets**: Character sprites and audio resources

### Key Components

1. **Band API**: Simplified interface for controlling virtual band members
2. **Code Editor**: Syntax-highlighting editor with debugging features
3. **Field View**: Real-time visualization of band formations
4. **Timeline**: Music synchronization system
5. **Scoring System**: Pride Points with multiplier mechanics
6. **Curriculum**: Structured lessons from basics to advanced concepts

### Contributing

We welcome contributions to Code of Pride! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
   ```bash
   pip install pytest
   ```

2. Run tests:
   ```bash
   python3 run_tests.py
   ```

3. Run specific test modules:
   ```bash
   python3 -m pytest tests/test_core_systems.py
   ```

## Curriculum Overview

The game teaches Python through 5 progressive modules:

### Module 1: First Rehearsal (Python Basics)
- Variables & Data Types
- Basic Commands & Functions
- Operators & Expressions

### Module 2: Learning the Drill (Control Flow)
- Conditional Statements
- Loops
- Loop Control

### Module 3: Section Leaders (Data Structures)
- Lists & List Methods
- Dictionaries
- Tuples & Sets

### Module 4: Advanced Choreography (Functions & Modules)
- Defining Functions
- Importing Modules
- Function Arguments & Scope

### Module 5: The Championship Show (Object-Oriented Programming)
- Classes & Objects
- Inheritance
- Polymorphism

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the educational approach of games like CodeCombat and Scratch
- Retro pixel art style inspired by Retro Bowl
- Marching band simulation informed by real drill design software
- Special thanks to marching band directors and performers who provided feedback

## Contact

For questions, feedback, or support, please contact:
- Email: support@codeofpride.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/code-of-pride/issues)

## Screenshots

![Gameplay Screenshot](docs/screenshots/gameplay.png)
*Writing Python code to control band formations*

![Editor Screenshot](docs/screenshots/editor.png)
*Syntax-highlighting code editor with debugging features*

![Field View](docs/screenshots/field.png)
*Real-time visualization of band formations*

---

*Code of Pride: Make learning Python a performance to remember!*
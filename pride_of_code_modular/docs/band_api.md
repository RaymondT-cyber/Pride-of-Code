# Band API Documentation

The Band API is the core interface that allows players to control virtual band members in Code of Pride. This document provides a comprehensive reference for all available methods and properties.

## Overview

The Band API provides a simplified interface for controlling band members on the field. All methods are accessible through the global `band` object when writing code in the game.

## Band Member Properties

Each band member has the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `id` | int | Unique identifier for the member |
| `x` | float | X position in yards (0-100) |
| `y` | float | Y position in yards (0-53.33) |
| `section` | str | Section name ('brass', 'woodwind', 'percussion', 'guard') |
| `instrument` | str | Specific instrument type |
| `facing` | int | Direction in degrees (0-359, 0 = up field) |

## Band API Methods

### Getting Members

#### `band.get_member(id)`
Get a specific band member by ID.

**Parameters:**
- `id` (int): Member ID (0 to band size - 1)

**Returns:**
- `BandMember` object or `None` if not found

**Example:**
```python
# Get the first band member
member = band.get_member(0)
```

#### `band.get_all_members()`
Get all band members.

**Returns:**
- List of all `BandMember` objects

**Example:**
```python
# Get all members
members = band.get_all_members()
```

#### `band.get_section(section_name)`
Get all members of a specific section.

**Parameters:**
- `section_name` (str): Section name ('brass', 'woodwind', 'percussion', 'guard')

**Returns:**
- List of `BandMember` objects in the specified section

**Example:**
```python
# Get all brass players
brass_players = band.get_section('brass')
```

### Moving Members

#### `band.move_to(member, x, y)`
Move a band member to a specific position.

**Parameters:**
- `member` (BandMember or int): Member object or ID
- `x` (float): X coordinate in yards (0-100)
- `y` (float): Y coordinate in yards (0-53.33)

**Example:**
```python
# Move member 0 to center field
band.move_to(0, 50, 26)

# Move member object to sideline
member = band.get_member(1)
band.move_to(member, 20, 10)
```

#### `band.move_forward(member, steps)`
Move a band member forward by a number of steps.

**Parameters:**
- `member` (BandMember or int): Member object or ID
- `steps` (int): Number of steps to move (negative = backward)

**Example:**
```python
# Move member forward 5 steps
member = band.get_member(0)
band.move_forward(member, 5)

# Move member backward 3 steps
band.move_forward(1, -3)
```

#### `band.turn(member, direction)`
Turn a band member to face a direction.

**Parameters:**
- `member` (BandMember or int): Member object or ID
- `direction` (str or int): Direction to face
  - String options: 'left', 'right', 'forward', 'backward'
  - Integer: Angle in degrees (0-359)

**Example:**
```python
# Turn member to face right
member = band.get_member(0)
band.turn(member, 'right')

# Turn member to face 45 degrees
band.turn(1, 45)
```

### Formations

#### `band.form_line(members, start_x, start_y, end_x, end_y)`
Arrange members in a straight line between two points.

**Parameters:**
- `members` (list): List of BandMember objects or IDs
- `start_x` (float): Starting X coordinate
- `start_y` (float): Starting Y coordinate
- `end_x` (float): Ending X coordinate
- `end_y` (float): Ending Y coordinate

**Example:**
```python
# Form a horizontal line with first 5 members
members = band.get_all_members()[:5]
band.form_line(members, 20, 26, 80, 26)
```

#### `band.form_circle(members, center_x, center_y, radius)`
Arrange members in a circle.

**Parameters:**
- `members` (list): List of BandMember objects or IDs
- `center_x` (float): Center X coordinate
- `center_y` (float): Center Y coordinate
- `radius` (float): Radius in yards

**Example:**
```python
# Form a circle with all brass players
brass = band.get_section('brass')
band.form_circle(brass, 50, 26, 10)
```

#### `band.form_block(members, x, y, rows, spacing=5.0)`
Arrange members in a rectangular block.

**Parameters:**
- `members` (list): List of BandMember objects or IDs
- `x` (float): Top-left corner X coordinate
- `y` (float): Top-left corner Y coordinate
- `rows` (int): Number of rows
- `spacing` (float, optional): Space between members in yards (default: 5.0)

**Example:**
```python
# Form a 2x4 block with woodwinds
woodwinds = band.get_section('woodwind')
band.form_block(woodwinds, 30, 20, 2)
```

## Examples

### Basic Movement
```python
# Move individual members
member1 = band.get_member(0)
member2 = band.get_member(1)

band.move_to(member1, 50, 26)  # Center field
band.move_to(member2, 20, 10)  # Left sideline
```

### Section Control
```python
# Move all brass players to form a line
brass = band.get_section('brass')
band.form_line(brass, 20, 30, 80, 30)

# Move all percussion to form a block
percussion = band.get_section('percussion')
band.form_block(percussion, 40, 15, 2)
```

### Complex Formation
```python
# Create a complex formation with multiple sections
brass = band.get_section('brass')
woodwinds = band.get_section('woodwind')
percussion = band.get_section('percussion')

# Brass forms a circle
band.form_circle(brass, 50, 26, 15)

# Woodwinds form a line
band.form_line(woodwinds, 20, 10, 80, 10)

# Percussion forms a block
band.form_block(percussion, 45, 40, 1, 3)
```

### Using Loops
```python
# Move all members forward 3 steps
members = band.get_all_members()
for member in members:
    band.move_forward(member, 3)

# Turn all brass players
brass = band.get_section('brass')
for member in brass:
    band.turn(member, 90)  # Turn right
```

## Best Practices

### Positioning
- Keep members within field boundaries (0-100 yards horizontally, 0-53.33 yards vertically)
- Maintain adequate spacing between members for visibility
- Consider the 8-yard movement per step when planning formations

### Efficiency
- Use section methods to control groups rather than individual members when possible
- Use loops to avoid repetitive code
- Combine formation methods for complex arrangements

### Debugging
- Use `print()` statements to check member positions
- Test formations incrementally
- Use the coordinate display (Ctrl+C) to verify positions

## Error Handling

The Band API includes basic error handling:

- Invalid member IDs will be ignored
- Out-of-bounds coordinates will be clamped to field boundaries
- Invalid section names will return empty lists
- Method calls with incorrect parameters will raise appropriate errors

## Advanced Usage

### Custom Formations
```python
# Create a custom formation function
def form_triangle(members, x, y, size):
    if len(members) < 3:
        return
    
    # Top point
    band.move_to(members[0], x, y - size)
    
    # Bottom left
    band.move_to(members[1], x - size, y + size)
    
    # Bottom right
    band.move_to(members[2], x + size, y + size)
    
    # Move remaining members to center
    for i in range(3, len(members)):
        band.move_to(members[i], x, y)

# Use the custom formation
members = band.get_all_members()[:6]
form_triangle(members, 50, 26, 10)
```

### Animation Effects
```python
# Create a simple animation with timing
import time

members = band.get_all_members()
for i, member in enumerate(members):
    band.move_to(member, 20 + i*5, 26)
    time.sleep(0.5)  # This would be simulated in the game
```

This documentation provides a comprehensive guide to using the Band API in Code of Pride. For more examples and advanced techniques, refer to the in-game lessons and challenges.
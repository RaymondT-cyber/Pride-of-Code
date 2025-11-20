# Lesson 1.1: Variables & Data Types
# Challenge: Move a band member to the 50-yard line

# Get the first band member
member = members[0]

# Create variables for position
x_position = 50  # 50-yard line (center)
y_position = 26  # Middle of field

# Move the member to the position
band.move_to(member, x_position, y_position)

# Print the result
print(f'Member moved to ({x_position}, {y_position})')
print('Challenge complete!')
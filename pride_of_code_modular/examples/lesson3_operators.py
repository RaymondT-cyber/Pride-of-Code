# Lesson 1.3: Operators & Expressions
# Challenge: Calculate the center of the field

# Field boundaries
left_sideline = 0
right_sideline = 100
back_sideline = 0
front_sideline = 53.33

# Calculate the center using arithmetic operators
center_x = (left_sideline + right_sideline) / 2
center_y = (back_sideline + front_sideline) / 2

print(f'Field center: ({center_x}, {center_y})')

# Move a member to the exact center
member = members[0]
band.move_to(member, center_x, center_y)

print('Member positioned at field center!')
print('Challenge complete!')
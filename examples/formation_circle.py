# Example: Create a circular formation
# This demonstrates using the form_circle() function

# Get all members
all_members = members

# Form a large circle at the 50-yard line
center_x = 50
center_y = 26.67
radius = 18  # yards

band.form_circle(all_members, center_x, center_y, radius)

print(f'Circle formed with {len(all_members)} members')
print(f'Center: ({center_x}, {center_y})')
print(f'Radius: {radius} yards')
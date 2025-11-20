# Lesson 1.2: Basic Commands & Functions
# Challenge: Form a line with the brass section

# Get all brass members
brass_members = brass

# Form them into a line from (20,20) to (80,20)
band.form_line(brass_members, 20, 20, 80, 20)

print(f'Brass section formed with {len(brass_members)} members')
print('Challenge complete!')
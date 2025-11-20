# Example: Multi-section formation
# This demonstrates controlling different sections independently

# Brass forms a line at the front
band.form_line(brass, 20, 15, 80, 15)
print(f'Brass line: {len(brass)} members')

# Woodwind forms a circle in the middle
band.form_circle(woodwind, 50, 26, 10)
print(f'Woodwind circle: {len(woodwind)} members')

# Percussion forms a block at the back
band.form_block(percussion, 35, 38, 2, 10)
print(f'Percussion block: {len(percussion)} members')

# Color guard forms a diagonal line
band.form_line(guard, 20, 35, 80, 45)
print(f'Guard diagonal: {len(guard)} members')

print('\nMulti-section formation complete!')
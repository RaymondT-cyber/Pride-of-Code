# Example: Advanced choreography with all sections
# This demonstrates a complex, multi-part drill

# Part 1: Opening formation - All sections in blocks
print('Part 1: Opening blocks...')
band.form_block(brass, 20, 15, 2, 8)
band.form_block(woodwind, 20, 25, 2, 8)
band.form_block(percussion, 20, 35, 2, 8)
band.form_block(guard, 60, 25, 2, 8)

# Part 2: Transition - Sections form lines
print('Part 2: Line transition...')
band.form_line(brass, 15, 20, 85, 20)
band.form_line(woodwind, 15, 26, 85, 26)
band.form_line(percussion, 15, 32, 85, 32)
band.form_line(guard, 15, 38, 85, 38)

# Part 3: Finale - Grand circle
print('Part 3: Grand circle finale...')
all_members = members
band.form_circle(all_members, 50, 26.67, 20)

print(f'\nChoreography complete! {len(all_members)} members in formation.')
print('This is what a real drill design looks like!')
#!/usr/bin/env python3
"""Demo script to showcase Code of Pride features."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from gameplay.code_executor import CodeExecutor
from ui.field_view import FieldView
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_GOLD, COLOR_TEXT,
    FIELD_OFFSET_X, FIELD_OFFSET_Y, FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT
)


def run_demo():
    """Run a visual demo of the game's capabilities."""
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Code of Pride - Demo")
    clock = pygame.time.Clock()
    
    # Initialize systems
    executor = CodeExecutor()
    field_view = FieldView(
        FIELD_OFFSET_X // 2, FIELD_OFFSET_Y,
        FIELD_PIXEL_WIDTH, FIELD_PIXEL_HEIGHT
    )
    
    font_title = pygame.font.SysFont('arial', 32, bold=True)
    font_code = pygame.font.SysFont('consolas', 14)
    font_normal = pygame.font.SysFont('arial', 16)
    
    # Demo scenarios
    demos = [
        {
            'title': 'Demo 1: Simple Movement',
            'code': [
                "# Move first member to center",
                "member = members[0]",
                "band.move_to(member, 50, 26)",
                "print('Center positioned!')"
            ]
        },
        {
            'title': 'Demo 2: Section Formation',
            'code': [
                "# Form brass in a line",
                "band.form_line(brass, 20, 20, 80, 20)",
                "print(f'Brass line: {len(brass)} members')"
            ]
        },
        {
            'title': 'Demo 3: Circle Formation',
            'code': [
                "# Form circle with all members",
                "band.form_circle(members, 50, 26, 20)",
                "print('Circle formation complete!')"
            ]
        },
        {
            'title': 'Demo 4: Block Formation',
            'code': [
                "# Create a marching block",
                "band.form_block(members, 30, 15, 4, 10)",
                "print('Block formation ready!')"
            ]
        },
        {
            'title': 'Demo 5: Complex Pattern',
            'code': [
                "# Multi-section pattern",
                "band.form_circle(brass, 30, 26, 10)",
                "band.form_circle(woodwind, 70, 26, 10)",
                "band.form_line(percussion, 45, 15, 55, 15)",
                "band.form_line(guard, 45, 38, 55, 38)",
                "print('Complex formation complete!')"
            ]
        }
    ]
    
    current_demo = 0
    output_text = "Press SPACE to run demo, N for next demo, ESC to quit"
    
    # Initial band setup
    executor.reset()
    executor.band_api.create_band(16)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Run current demo
                    demo = demos[current_demo]
                    code = '\n'.join(demo['code'])
                    success, output = executor.execute(code, 16)
                    output_text = f"✓ {output}" if success else f"✗ {output}"
                elif event.key == pygame.K_n:
                    # Next demo
                    current_demo = (current_demo + 1) % len(demos)
                    executor.reset()
                    executor.band_api.create_band(16)
                    output_text = "Press SPACE to run this demo"
                elif event.key == pygame.K_r:
                    # Reset
                    executor.reset()
                    executor.band_api.create_band(16)
                    output_text = "Band reset to starting formation"
        
        # Draw
        screen.fill(COLOR_BG)
        
        # Title
        demo = demos[current_demo]
        title = font_title.render(demo['title'], True, COLOR_GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        screen.blit(title, title_rect)
        
        # Code display
        code_y = 80
        for i, line in enumerate(demo['code']):
            code_surf = font_code.render(line, True, COLOR_TEXT)
            screen.blit(code_surf, (20, code_y + i * 20))
        
        # Field view
        members = executor.get_band_members()
        field_view.draw(screen, members)
        
        # Output
        output_lines = output_text.split('\n')
        output_y = WINDOW_HEIGHT - 80
        for line in output_lines[:3]:
            text = font_normal.render(line, True, COLOR_TEXT)
            screen.blit(text, (20, output_y))
            output_y += 22
        
        # Instructions
        instructions = font_normal.render(
            f"SPACE: Run | N: Next ({current_demo+1}/{len(demos)}) | R: Reset | ESC: Quit",
            True, (150, 150, 150)
        )
        screen.blit(instructions, (20, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n✓ Demo completed!")
    print("\nTo play the full game, run: python3 core/main.py")


if __name__ == '__main__':
    print("="*60)
    print("  CODE OF PRIDE - Interactive Demo")
    print("="*60)
    print("\nThis demo showcases the game's core features:")
    print("  • Real-time Python code execution")
    print("  • Visual band member control")
    print("  • Formation algorithms")
    print("  • Retro pixel art style")
    print("\nStarting demo...\n")
    
    try:
        run_demo()
    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()
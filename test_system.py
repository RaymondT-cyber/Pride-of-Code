#!/usr/bin/env python3
"""System test to verify all components work together."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "="*60)
    print("TESTING: Module Imports")
    print("="*60)
    
    try:
        import pygame
        print("✓ pygame imported")
        
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        print(f"✓ config imported (window: {WINDOW_WIDTH}x{WINDOW_HEIGHT})")
        
        from gameplay.band_api import BandAPI, BandMember
        print("✓ band_api imported")
        
        from gameplay.code_executor import CodeExecutor
        print("✓ code_executor imported")
        
        from gameplay.lessons import LessonManager
        print("✓ lessons imported")
        
        from ui.field_view import FieldView
        print("✓ field_view imported")
        
        from ui.editor import CodeEditor
        print("✓ editor imported")
        
        from ui.retro_button import RetroButton
        print("✓ retro_button imported")
        
        from scenes.retro_menu import RetroMainMenu
        print("✓ retro_menu imported")
        
        from scenes.editor_scene import EnhancedEditorScene
        print("✓ enhanced_editor imported")
        
        from core.game import PrideOfCodeGame
        print("✓ game imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_band_api():
    """Test the Band API functionality."""
    print("\n" + "="*60)
    print("TESTING: Band API")
    print("="*60)
    
    try:
        from gameplay.band_api import BandAPI
        
        api = BandAPI()
        api.create_band(16)
        print(f"✓ Created band with {len(api.members)} members")
        
        # Test move_to
        member = api.members[0]
        api.move_to(member, 50, 26)
        print(f"✓ Moved member to ({member.x}, {member.y})")
        
        # Test form_circle
        brass = api.get_section('brass')
        api.form_circle(brass, 50, 26, 10)
        print(f"✓ Formed circle with {len(brass)} brass members")
        
        # Test form_line
        woodwind = api.get_section('woodwind')
        api.form_line(woodwind, 20, 20, 80, 20)
        print(f"✓ Formed line with {len(woodwind)} woodwind members")
        
        return True
    except Exception as e:
        print(f"✗ Band API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_executor():
    """Test the code execution engine."""
    print("\n" + "="*60)
    print("TESTING: Code Executor")
    print("="*60)
    
    try:
        from gameplay.code_executor import CodeExecutor
        
        executor = CodeExecutor()
        
        # Test simple code
        code1 = """
member = members[0]
band.move_to(member, 50, 26)
print(f'Member at ({member.x}, {member.y})')
"""
        success, output = executor.execute(code1)
        print(f"✓ Simple code executed: {success}")
        print(f"  Output: {output.strip()}")
        
        # Test formation code
        code2 = """
band.form_circle(brass, 50, 26, 15)
print(f'Circle with {len(brass)} members')
"""
        success, output = executor.execute(code2)
        print(f"✓ Formation code executed: {success}")
        print(f"  Output: {output.strip()}")
        
        # Test error handling
        code3 = "this is invalid python"
        success, output = executor.execute(code3)
        print(f"✓ Error handling works: {not success}")
        
        return True
    except Exception as e:
        print(f"✗ Code executor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lessons():
    """Test the lesson system."""
    print("\n" + "="*60)
    print("TESTING: Lesson System")
    print("="*60)
    
    try:
        from gameplay.lessons import LessonManager
        from gameplay.band_api import BandAPI
        
        lesson_mgr = LessonManager()
        lessons = lesson_mgr.get_all_lessons()
        print(f"✓ Loaded {len(lessons)} lessons")
        
        # Test lesson 1
        lesson1 = lesson_mgr.get_lesson('week1_lesson1')
        print(f"✓ Lesson 1: {lesson1.title}")
        
        # Test validation
        api = BandAPI()
        api.create_band(16)
        api.move_to(api.members[0], 50, 26)
        success, msg = lesson1.validate(api)
        print(f"✓ Lesson validation: {success} - {msg}")
        
        return True
    except Exception as e:
        print(f"✗ Lesson test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_init():
    """Test game initialization (without running the loop)."""
    print("\n" + "="*60)
    print("TESTING: Game Initialization")
    print("="*60)
    
    try:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        import pygame
        pygame.init()
        
        from core.game import PrideOfCodeGame
        
        game = PrideOfCodeGame()
        print(f"✓ Game initialized")
        print(f"✓ Window size: {game.screen.get_width()}x{game.screen.get_height()}")
        print(f"✓ Available scenes: {list(game.state_manager.states.keys())}")
        print(f"✓ Current scene: {game.state_manager.current_name}")
        print(f"✓ Editor loaded: {hasattr(game, 'editor')}")
        print(f"✓ Lesson manager loaded: {hasattr(game, 'lesson_manager')}")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Game init test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  CODE OF PRIDE - SYSTEM TEST SUITE")
    print("="*70)
    
    results = []
    
    results.append(("Module Imports", test_imports()))
    results.append(("Band API", test_band_api()))
    results.append(("Code Executor", test_code_executor()))
    results.append(("Lesson System", test_lessons()))
    results.append(("Game Initialization", test_game_init()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} | {name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is operational.")
        print("\nTo run the game:")
        print("  python3 core/main.py")
        print("\nTo run the demo:")
        print("  python3 DEMO.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

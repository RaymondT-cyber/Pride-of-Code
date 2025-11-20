import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from core.game import PrideOfCodeGame

def main():
    pygame.init()

    game = PrideOfCodeGame()
    game.run()      # Start main loop

    pygame.quit()

if __name__ == "__main__":
    main()

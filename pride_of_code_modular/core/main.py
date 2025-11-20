import pygame
from core.game import PrideOfCodeGame

def main():
    pygame.init()

    game = PrideOfCodeGame()
    game.run()      # Start main loop

    pygame.quit()

if __name__ == "__main__":
    main()

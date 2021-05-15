import sys
import pygame

from setting import Settings
from character import Character

class Seva:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))
        self.bg_color = (230,230,230)
        pygame.display.set_caption("Seva")

        self.settings = Settings()
        self.character = Character(self)

    
    def run_game(self):
        while True:
            self._update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)

        self.character.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
        
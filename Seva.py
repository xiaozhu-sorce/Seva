import sys
import pygame

from Setting import Settings

class Seva:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Seva")
    
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
            pygame.display.flip()
    
if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
        
import sys
import pygame

from setting import Settings
from character import Character
from time import sleep

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
            self._check_events()
            self._update_screen()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
        if event.key == pygame.K_LEFT:
            self.character.moving_left = False

    def _check_keydown_events(self,event):
        #左右移动
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
        #空格跳跃
        if event.key == pygame.K_SPACE:
            self.character.jump = True

        
    def _update_screen(self):
        self.screen.fill(self.bg_color)

        self.character.blitme()

        self.character.move_character()
        self.character.jump_up_character()

        pygame.display.flip()

if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
        
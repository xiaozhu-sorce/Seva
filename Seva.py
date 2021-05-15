import sys
import pygame
from boards import Board
from grass import Grass
from grassScore import GrassSore
from setting import Settings
from character import Character
from time import sleep

class Seva:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Seva")

        self.boards = [Board(self.screen, 100, 40, 800, 500),
                       Board(self.screen, 100, 40, 800, 500),
                       Board(self.screen, 40, 40, 1000, 400),
                       Board(self.screen, 200, 20, 600, 300),
                       Board(self.screen, 200, 40, 400, 280),
                       Board(self.screen, 100, 40, 100, 150)]
        self.grasses = [Grass(self.screen, 800, 460)]

        # 分数
        self.grass_score = GrassSore(self.screen)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

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

            # 更新
            self.boards[2].explosion()
            # 覆盖
            self.screen.fill((0, 0, 0))
            # 刷新
            for board in self.boards:
                board.blitme()
            for grass in self.grasses:
                grass.update_grass()
                self.grass_score.show_score()

<<<<<<< HEAD
            pygame.display.flip()
=======
        self.character.move_character()
        self.character.jump_up_character()
>>>>>>> b3db184eb3c861bce7bdd223ba9818cb8310564d

        pygame.display.flip()

if __name__ == '__main__':
    seva = Seva()
    seva.run_game()

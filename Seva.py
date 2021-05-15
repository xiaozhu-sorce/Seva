import sys
import pygame
from boards import Board
from grass import Grass
from grassScore import GrassSore

from Setting import Settings


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

            pygame.display.flip()


if __name__ == '__main__':
    seva = Seva()
    seva.run_game()

import pygame
import pygame.font
from grass import Grass


class GrassSore:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.grass = Grass(self.screen, 1100, 15)

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.score = 3

    def prep_score(self):
        self.score_image = self.font.render(str(self.score), True, self.text_color,
                                            (255, 255, 255))

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.grass.update_grass()

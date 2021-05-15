import pygame
import pygame.font
from grass import Grass, Heart


class GrassScore:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.grass = Grass(self.screen, 1100, 15)

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.grass_score = 0
        self.heart_score = 3

    def prep_score(self):
        self.score_image1 = self.font.render(str(self.grass_score), True, self.text_color,
                                             (255, 255, 255))

        self.score_rect1 = self.score_image1.get_rect()
        self.score_rect1.right = self.screen_rect.right - 20
        self.score_rect1.top = 20
        # 心
        self.score_image2 = self.font.render(str(self.heart_score), True, self.text_color,
                                             (255, 255, 255))

        self.score_rect2 = self.score_image2.get_rect()
        self.score_rect2.right = self.screen_rect.right - 120
        self.score_rect2.top = 20

    def show_score(self):
        self.screen.blit(self.score_image1, self.score_rect1)
        self.screen.blit(self.score_image2, self.score_rect2)
        grass = Grass(self.screen, 1100, 10)
        grass.update_grass()
        heart = Heart(self.screen, 1000, 10)
        heart.update_heart()



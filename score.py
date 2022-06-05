import pygame
import pygame.font


class Score:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.grass_score = 0
        self.heart_score = 3

    def prep_score(self):
        """计算草和花的个数"""
        # 草的个数
        self.score_grass = self.font.render(str(self.grass_score), True, self.text_color,
                                            (255, 255, 255))

        self.grass_score_rect = self.score_grass.get_rect()
        self.grass_score_rect.right = self.screen_rect.right - 20
        self.grass_score_rect.top = 20

        # 心的个数
        self.score_heart = self.font.render(str(self.heart_score), True, self.text_color,
                                            (255, 255, 255))

        self.heart_score_rect = self.score_heart.get_rect()
        self.heart_score_rect.right = self.screen_rect.right - 120
        self.heart_score_rect.top = 20

    def show_score(self):
        """绘制草和花"""
        self.screen.blit(self.score_grass, self.grass_score_rect)
        self.screen.blit(self.score_heart, self.heart_score_rect)

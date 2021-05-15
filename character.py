import pygame
from pygame.sprite import Sprite


class Character(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        # 访问屏幕属性
        self.screen_rect = ai_game.screen.get_rect()

        # 加载图像并获取矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 图像初始位置
        self.rect.bottomleft = self.screen_rect.bottomleft

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

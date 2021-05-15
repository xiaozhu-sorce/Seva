import pygame
from time import sleep
from pygame.sprite import Sprite
from setting import Settings

class Character(Sprite):
    g = 9.8

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 访问屏幕属性
        self.screen_rect = ai_game.screen.get_rect()

        # 加载图像并获取矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 图像初始位置
        self.rect.bottom = self.screen_rect.bottom - 100
        self.rect.left = self.screen_rect.left

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False

        self.jump = False

    def move_character(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left >= 0:
            self.x -= self.settings.character_speed

        self.rect.x = self.x

    def jump_up_character(self):
        if self.jump:
            # 玩家跳起
            if self.settings.character_jump_up >= 0:
                self.y -= self.settings.character_jump_up
                self.settings.character_jump_up -= 1
            # 玩家落地
            elif self.rect.y >= self.screen_rect.bottom - 100:
                self.settings.character_jump_up = 15
                self.settings.character_jump_down = 0
                self.jump = False
            # 玩家下落
            else:
                self.settings.character_jump_down += 1
                self.y += self.settings.character_jump_down
        self.rect.y = self.y
        sleep(0.025)
        print(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


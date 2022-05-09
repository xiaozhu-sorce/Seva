import pygame
from time import sleep
from pygame.sprite import Sprite


class Character(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.character_type = 1
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.rain = ai_game.rains
        # 访问屏幕属性
        self.screen_rect = ai_game.screen.get_rect()

        self.moving_right = False
        self.moving_left = False

        self.jump = False
        self.down = False

        self.reset()

    def move_character(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left >= 0:
            self.x -= self.settings.character_speed

        self.rect.x = self.x

    def jump_up_character(self):
        if self.jump:
            # 玩家跳起
            if self.settings.character_jump_up > 0:
                self.y -= self.settings.character_jump_up
                self.settings.character_jump_up -= 1
            if self.settings.character_jump_up == 0:
                self.jump = False
                self.down = True
        elif self.down:
            # 玩家落地
            if self.rect.y >= self.screen_rect.bottom - 163:
                self.settings.character_jump_up = 20
                self.settings.character_jump_down = 0
                self.jump = False
            # 玩家下落
            else:
                self.settings.character_jump_down += 1
                self.y += self.settings.character_jump_down

        self.rect.y = self.y
        sleep(0.002)

    def draw_character(self):
        self.screen.blit(self.image, self.rect)

    def update_character(self):
        # 加载图像并获取矩形
        self.image = pygame.image.load('images/person' + str(self.character_type) + '.png')

    def reset(self):
        self.character_type = 1
        self.update_character()
        self.rect = self.image.get_rect()
        # 图像初始位置
        self.rect.y = self.screen_rect.bottom - 163
        self.rect.x = self.screen_rect.left
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

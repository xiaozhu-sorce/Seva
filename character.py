import pygame
from time import sleep
from pygame.sprite import Sprite


class Character(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        # 访问游戏各属性
        self.character_type = 1
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.rain = ai_game.rains
        self.screen_rect = ai_game.screen.get_rect()

        self.moving_right = False
        self.moving_left = False

        self.jump = False
        self.down = False

        self.reset()

    def move_character(self):
        """按键控制人物左右移动"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left >= 0:
            self.x -= self.settings.character_speed

        self.rect.x = self.x

    def jump_up_character(self):
        """人物跳跃"""
        if self.jump:
            # 玩家跳起
            if self.settings.character_jump_up > 0:
                # 跳跃过程中
                self.y -= self.settings.character_jump_up
                self.settings.character_jump_up -= 1
            if self.settings.character_jump_up == 0:
                # 到达最高点
                self.jump = False
                self.down = True
        elif self.down:
            # 玩家下降
            if self.rect.y >= self.screen_rect.bottom - 163:
                # 没有碰到木板直接落地，初始化可以跳跃的高度和属性
                self.settings.character_jump_up = 20
                self.settings.character_jump_down = 0
            else:
                # 玩家下落
                self.settings.character_jump_down += 1
                self.y += self.settings.character_jump_down
        # 根据self.y更新rect对象
        self.rect.y = self.y
        sleep(0.01)

    def draw_character(self):
        self.screen.blit(self.image, self.rect)

    def update_character(self):
        """根据当前的状态加载图像并获取矩形"""
        self.image = pygame.image.load('images/person' + str(self.character_type) + '.png')

    def reset(self):
        """重新初始化对象"""
        self.character_type = 1
        self.update_character()
        self.rect = self.image.get_rect()
        # 图像初始位置
        self.rect.y = self.screen_rect.bottom - 163
        self.rect.x = self.screen_rect.left
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

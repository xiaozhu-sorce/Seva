import sys
from typing import ForwardRef
import pygame
import functions as fc
from rain import Rain
from random import randint
from setting import Settings
from character import Character
from time import sleep
from boards import Board
from grass import Grass
from score import GrassScore
from pulluted import Pulluted
from score import GrassScore
from pygame.sprite import Group

class Seva:

    def __init__(self):
        # 初始化
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.screen.fill(self.settings.bg_color)
        self.screen_rect = self.screen.get_rect()
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()

        self.rains = pygame.sprite.Group()
        self.character = Character(self)
        self.pulleted = Pulluted(self)

        self.rains_drop = True
        self.pulleted_up = False
        self.rain_height = 0
        self.option_type = 0
        self.screen_type = 0

        self.boards = [Board(self.screen, 100, 40, 800, 500),
                       Board(self.screen, 100, 40, 800, 500),
                       Board(self.screen, 40, 40, 1000, 400),
                       Board(self.screen, 200, 20, 600, 300),
                       Board(self.screen, 200, 40, 400, 280),
                       Board(self.screen, 100, 40, 100, 150)]

        self.grasses = pygame.sprite.Group()
        self.grasses.add(Grass(self.screen, 800, 460))

        # 分数
        self.grass_score = GrassScore(self.screen)

        pygame.display.set_caption("Seva")

    def run_game(self):
        self.create_rain()
        while True:
            self._check_plat()
            self._check_events()
            if self.screen_type == 0:
                self._update_screen_main()
            elif self.screen_type == 1:
                self._update_screen_1()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False

        if event.key == pygame.K_LEFT:
            self.character.moving_left = False

    def _check_keydown_events(self, event):
        # 左右移动
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
            self.option_type = 2

        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
            self.option_type = 1

        if event.key == pygame.K_RETURN:
            if self.option_type == 1:
                sys.exit()
            elif self.option_type == 2:
                self.screen_type = 1

        # 空格跳跃
        if event.key == pygame.K_SPACE:
            self.character.jump = True

    def _update_screen_main(self):
        self.image_bg1 = pygame.image.load('images/bg1.png')
        self.rect_bg1 = self.image_bg1.get_rect()
        self.rect_bg1.midbottom = self.screen_rect.midbottom
        self.screen.blit(self.image_bg1, self.rect_bg1)
        self._update_quit_and_next()

        pygame.display.flip()


    def _check_plat(self): 
        
        collision = pygame.sprite.spritecollide(self.character,self.boards,False)
        if collision:
            self.character.down = False
            self.settings.character_jump_down = 0
            for c in collision:
                if self.character.rect.top > c.rect.y:
                    self.character.jump = False
                    self.character.down = True
                elif self.character.rect.bottom > c.rect.y and self.character.jump == False:
                    self.settings.character_jump_up = 20
        else:
            self.character.down = True


    def _update_screen_1(self):
        self.screen.fill((255, 255, 255))  # 需要再绘制背景颜色，不然会有阴影

        self.character.blitme()
        self.character.move_character()
        self.character.jump_up_character()

        self.rains.draw(self.screen)
        self.rain_drop()
        self.check_rain_oracle()

        # 更新
        self.boards[2].explosion()
        # 刷新
        for board in self.boards:
            board.blitme()
        for grass in self.grasses:
            # 是否得到
            self.check_grass_gain(grass)
            # 更新小草数目
            self.grass_score.prep_score()
        # 遍历grasses刷新
        fc.update_grasses(self.grasses)
        self.grass_score.show_score()

        self._update_pulleted()

        pygame.display.flip()

    def _update_pulleted(self):
        """管理废水的类"""
        self.screen.blit(self.pulleted.image, self.pulleted.rect)
        if self.pulleted_up:
            if (self.pulleted.rect.y >= self.screen_rect.top+50):
                self.pulleted.rect.y -= self.settings.pulluted_speed

    def create_rain(self):
        """
        判断行列有多少元素,设置间距,生产雨添加到Group组
        """
        new_rain = Rain(self)
        self.rain_height = new_rain.rect_height
        m = 0
        for x in range(5):
            m += 200
            new_rain = Rain(self)
            random_number = randint(-100, 100)
            new_rain.rect.x = m + random_number
            self.rains.add(new_rain)

    def rain_drop(self):
        # 更新雨下落的Y轴位置
        for read_rain in self.rains.sprites():

            read_rain.rect.y += 1.0
            if read_rain.rect.y >= 150:

                self.rains_drop = True
            else:
                self.rains_drop = False

    def check_rain_oracle(self):
        # 检查是否到达边界，删除到达边界的元素
        for read_rain in self.rains.copy():
            if read_rain.rect.bottom >= self.screen_height:
                self.rains.remove(read_rain)
                self.pulleted_up = True
                
        if self.rains_drop:
            self.create_rain()

    def check_grass_changeable(self):
        if self.grass_score.grass_score >= 3:
            self.grass_score.change_grass()

        self.grass_score.update_grass()

    def check_grass_gain(self, grass):
        # 碰撞
        collisions = pygame.sprite.spritecollide(self.character, self.grasses, True)
        if collisions:
            # 大于3减少3棵草（兑换心）
            if self.grass_score.grass_score >= 3:
                self.grass_score.grass_score -= 3
                self.grass_score.heart_score += 1
            else:
                self.grass_score.grass_score += 1

    def _update_quit_and_next(self):
        if self.option_type == 0:
            self.image_quit = pygame.image.load('images/title2(un).png')
            self.image_next = pygame.image.load('images/title1(un).png')
        elif self.option_type == 1:
            self.image_quit = pygame.image.load('images/title2.png')
            self.image_next = pygame.image.load('images/title1(un).png')
        elif self.option_type == 2:
            self.image_quit = pygame.image.load('images/title2(un).png')
            self.image_next = pygame.image.load('images/title1.png')

        self.rect_quit = self.image_quit.get_rect()
        self.rect_next = self.image_next.get_rect()
        
        self.rect_quit.bottomleft = self.screen_rect.midbottom
        self.rect_next.bottomright = self.screen_rect.bottomright
        
        self.screen.blit(self.image_quit, self.rect_quit)
        self.screen.blit(self.image_next, self.rect_next)

if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
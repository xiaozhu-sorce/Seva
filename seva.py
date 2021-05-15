import sys
import pygame
from rain import Rain
from random import randint
from setting import Settings
from character import Character
from time import sleep
 
class Seva:

    def __init__(self):
        #初始化
        pygame.init()
        self.settings = Settings()
 
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        self.screen.fill(self.settings.bg_color)
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        
        self.rains= pygame.sprite.Group()
        self.character = Character(self)

        self.rains_drop = True
        self.rain_height = 0

        pygame.display.set_caption("Seva")

    def run_game(self):
        self.create_rain()
        while True:
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
        self.screen.fill((255, 255, 255))  # 需要再绘制背景颜色，不然会有阴影
        
        self.character.blitme()

        self.character.move_character()
        self.character.jump_up_character()

        self.rains.draw(self.screen)#将雨的组集体绘制
        self.rain_drop()#更新下落
        self.check_rain_oracle()#检查是否到达边界

        pygame.display.flip()

    def create_rain(self):
        """
        判断行列有多少元素
        设置间距
        生产雨添加到Group组
        """
        new_rain = Rain(self)
        self.rain_height = new_rain.rect_height
        m = 0
        for x in range(11):
            m+=100
            new_rain = Rain(self)
            random_number = randint(-20, 20)
            new_rain.rect.x = m + random_number
            self.rains.add(new_rain)

    def rain_drop(self):
        #更新雨下落的Y轴位置
        for read_rain in self.rains.sprites():
            read_rain.rect.y += 1.0
            if read_rain.rect.y >= 100:
                self.rains_drop = True
            else:
                self.rains_drop = False
            sleep(0.00001)
 
    def check_rain_oracle(self):
        #检查是否到达边界，删除到达边界的元素
        for read_rain in self.rains.copy():
            if read_rain.rect.bottom >= self.screen_height :
                self.rains.remove(read_rain)
        if self.rains_drop:
            self.create_rain()
 
if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
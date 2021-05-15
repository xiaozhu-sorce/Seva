import pygame


class Settings:
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # 雨滴速度
        self.rain_speed = 1.0

        self.character_speed = 7  # 在80的跳跃高度下，水平移动大约为220
        self.character_jump_up = 20  # 跳跃高度大约为80
        self.character_jump_down = 0

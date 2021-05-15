import pygame

class Settings:
    def __init__(self):
        """初始化游戏的设置"""
		#屏幕设置
        self.screen_width = 1200
        self.screen_height = 800    
        self.bg_color = (230,230,230)

        #雨滴速度
        self.rain_speed = 1.0
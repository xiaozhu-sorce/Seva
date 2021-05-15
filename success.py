
import pygame
from pygame.sprite import Sprite

class Door(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 访问屏幕属性
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/spike2.png')
        self.rect = self.image.get_rect()

        self.rect.right = self.screen_rect.right
        self.rect.top = 500

    def show_door(self):
        self.screen.blit(self.image,self.rect)

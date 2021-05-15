import pygame
from pygame.sprite import Sprite
 
class Rain(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/rain.bmp')
        self.rect = self.image.get_rect()
        self.rect_width = self.rect.width
        self.rect_height = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
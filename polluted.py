import pygame
from pygame.sprite import Sprite


class Polluted(Sprite):

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.polluted_up = False

        self.image = pygame.image.load('images/polluted.png')
        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midbottom

    def update_pulleted(self):
        """管理废水的方法"""
        self.screen.blit(self.image,self.rect)
        if self.polluted_up:
            if self.rect.y >= self.screen_rect.top + 50:
                self.rect.y -= self.settings.polluted_speed

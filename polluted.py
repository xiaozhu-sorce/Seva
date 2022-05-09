import pygame
from pygame.sprite import Sprite


class Polluted(Sprite):

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/polluted.png')
        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midbottom

import pygame


class Board:
    def __init__(self, screen, width, length, x, y):
        self.screen = screen

        self.image = pygame.image.load('image2/board1.bmp')
        self.image = pygame.transform.scale(self.image, (width, length))
        # self.screen_rect = screen.get_rect()
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

    def explosion(self):
        self.rect.y += 1

    def blitme(self):
        self.screen.blit(self.image, self.rect)

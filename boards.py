import pygame


class Board:
    def __init__(self, screen, width, length, x, y, ifWarning=False):
        self.screen = screen
        self.ifWarning = ifWarning
        if ifWarning:
            self.image_warning = pygame.image.load('images/brick/brick2_warning.png')
            self.image_warning = pygame.transform.scale(self.image_warning, (width, length))
            self.rect = self.image_warning.get_rect()
        else:
            self.image = pygame.image.load('images/brick/brick2.png')
            self.image = pygame.transform.scale(self.image, (width, length))
            self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

    def explosion(self):
        self.rect.y += 1

    def blitme(self):
        if self.ifWarning:
            self.screen.blit(self.image_warning, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

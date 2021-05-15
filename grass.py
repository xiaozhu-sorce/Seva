import pygame


class Grass(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        self.image = pygame.image.load('images/spike2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_grass(self):
        self.screen.blit(self.image, self.rect)


class Heart:
    def __init__(self, screen, x, y):
        self.screen = screen

        self.image = pygame.image.load('image2/heart.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_heart(self):
        self.screen.blit(self.image, self.rect)

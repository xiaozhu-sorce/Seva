import pygame

class Grass:
    def __init__(self, screen, x, y):
        self.screen = screen

        self.image = pygame.image.load('image2/grass.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_grass(self):
        self.screen.blit(self.image, self.rect)

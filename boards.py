import pygame


class Board:
    def __init__(self, screen, width, length, x, y, ifWarning=False):

        self.screen = screen
        self.ifWarning = ifWarning
        self.if_explode = False
        # 移动速度、方向
        self.move_speed = 5
        self.direction = 1

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
        self.x = float(self.rect.x)

    def explosion(self):
        self.rect.y += 10

    def move_left_right(self):
        self.x += self.move_speed * self.direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def draw_boards(self, board):
        if self.ifWarning:
            if self.if_explode:
                board.explosion()
            self.screen.blit(self.image_warning, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

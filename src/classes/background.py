import pygame


class BackGround:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def set_image(self, src):
        self.image = pygame.image.load(src)
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.image, self.rect)

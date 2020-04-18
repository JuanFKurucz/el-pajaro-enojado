import pygame


class BackGround:
    Objects = []

    def __init__(self, x, y, img):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        BackGround.Objects.append(self)

    @classmethod
    def draw(cls, screen):
        for o in BackGround.Objects:
            screen.blit(o.image, o.rect)

    @classmethod
    def Clean(cls):
        BackGround.Objects = []

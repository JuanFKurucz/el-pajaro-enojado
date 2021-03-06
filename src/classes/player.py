import pygame, math


from src.config import FLOOR, HEIGHT
from src.classes.enemy import Enemy


class Player:
    # Clase de jugador
    def __init__(self, img, fuerza, angulo):
        self.image = pygame.image.load(img)  # Se carga la imagen del jugadorS
        self.width = 21
        self.height = 21
        self.x = 0
        self.y = HEIGHT - self.height - FLOOR
        self.score = 0
        self.fuerza = fuerza
        self.angulo = angulo
        # Se hace el calculo de vx y vy
        self.vx = round((fuerza * math.cos(math.radians(angulo))), 2)
        self.vy = round((fuerza * math.sin(math.radians(angulo))), 2)

        self.rect = self.image.get_rect()  # Se consigue el cuerpo del jugador para moverlo
        self.rect.x = self.x
        self.rect.y = self.y

    def check_collision(self, elements):
        # Funcion de colision de jugador con cajas
        for enemy in elements:
            if (
                self.rect.x < enemy.rect.right
                and self.rect.right > enemy.rect.x
                and self.rect.y < enemy.rect.bottom
                and self.rect.bottom > enemy.rect.y
            ):
                # Si la caja esta siendo dibujada y el jugador se encuentra dentro de la caja
                self.score += 1
                enemy.destroy()

    def draw(self, screen):
        screen.blit(
            self.image, self.rect
        )  # Se dibuja en pantalla la imagen del jugador con su cuerpo

import pygame, math


from src.config import FLOOR, HEIGHT


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

    def CheckCol(self, elements):
        # Funcion de colision de jugador con cajas
        for e in elements:
            if (
                e.dibujado == True
                and self.rect.x < e.rect.right
                and self.rect.right > e.rect.x
                and self.rect.y < e.rect.bottom
                and self.rect.bottom > e.rect.y
            ):
                # Si la caja esta siendo dibujada y el jugador se encuentra dentro de la caja
                self.score += 1
                e.destroy()

    def draw(self, screen):
        screen.blit(
            self.image, self.rect
        )  # Se dibuja en pantalla la imagen del jugador con su cuerpo

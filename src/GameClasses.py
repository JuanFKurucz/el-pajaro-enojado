import pygame, math
from Global import *


class Player:
    # Clase de jugador
    def __init__(self, img, fuerza, angulo):
        self.image = pygame.image.load(img)  # Se carga la imagen del jugadorS
        self.width = 21
        self.height = 21
        self.x = 0
        self.y = height - self.height - floor
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


class Enemys:
    listE = []  # Lista donde se guardaran objetos caja
    destroyed = 0  # Conteo de cuantos se destruyeron en total
    falling = False  # Si hay cajas cayendo

    def __init__(self, x, y, img):
        self.image = pygame.image.load(img)
        self.x = x
        self.y = y - floor
        self.width = 15
        self.height = 15
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dibujado = True
        self.ti = (
            0  # Se creara un movimiento de caida libre con un tiempo inicial obtenido a futuro
        )
        Enemys.listE.append(self)

    def destroy(self):
        # Funcion que es llamada cuando el jugador colisiona con la caja
        if self.dibujado == True:
            self.dibujado = False
            Enemys.destroyed += 1

    def draw(self, screen):
        # Dibujado en pantalla
        if self.dibujado == True:
            screen.blit(self.image, self.rect)

    @classmethod
    def CheckCol(cls, time):
        # Funcion de colisiones entre cajas y gravedad de las mismas
        fallingCheck = 0  # Si hay cajas cayendo
        for e in range(len(Enemys.listE)):
            # por cada caja en la lista de cajas
            # Como las cajas estan astutamente creadas en columnas de forma
            # 			11	10	9
            # 			8	7	6
            # 			5	4	3
            # 			2	1	0
            #
            # Podemos obtener la caja que tiene abajo haciendo el indice de esta caja -3
            # Se realizo de esta forma para poder hacer real el movimiento de cada caja ya que se actualiza en orden de caida
            multiplicador = 3
            while e - multiplicador >= 0 and Enemys.listE[e - multiplicador].dibujado == False:
                # no se esta dibujando se chequea la siguiente debido a que quiere decir que el jugador impacto con la misma.
                multiplicador += 3
            if e - multiplicador >= 0:
                # Si el indice de la caja existe
                if (
                    Enemys.listE[e].rect.bottom <= Enemys.listE[e - multiplicador].rect.y
                    and Enemys.listE[e - multiplicador].rect.y - Enemys.listE[e].rect.bottom != 0
                ):
                    # Colision contra la siguiente caja
                    if Enemys.listE[e].ti == 0:
                        Enemys.listE[e].ti = time  # Se asgina el tiempo inicial
                    # Movimiento de caida libre mruv
                    Enemys.listE[e].rect.y = Enemys.listE[e].y + (g / 2) * (
                        ((time - Enemys.listE[e].ti) / 1000.0) ** 2
                    )
                    fallingCheck += 1
            elif Enemys.listE[e].rect.bottom < height - floor:
                # Si no cae hasta tocar contra el suelo debido a que no tiene mas cajas abajo
                if Enemys.listE[e].ti == 0:
                    Enemys.listE[e].ti = time  # Se asgina el tiempo inicial
                # Movimiento de caida libre mruv
                Enemys.listE[e].rect.y = Enemys.listE[e].y + (g / 2) * (
                    ((time - Enemys.listE[e].ti) / 1000.0) ** 2
                )
                fallingCheck += 1
        else:
            if fallingCheck > 0:
                # Si hay cajas cayendo
                Enemys.falling = True
            else:
                Enemys.falling = False

    @classmethod
    def Clean(cls):
        # Funcion que limpia los objetos cajas y resetea el estado de caida
        Enemys.falling = False
        Enemys.listE = []


class Graphs:
    Array = []
    active = True

    def __init__(self, x, t1, t2, scale, textfunc, past, final, finalT):
        if len(Graphs.Array) - 1 >= 0:
            # Si existen graficas creadas se asigna a la derecha de la misma
            self.x = (
                Graphs.Array[len(Graphs.Array) - 1].x
                + Graphs.Array[len(Graphs.Array) - 1].width
                + x
            )
        else:
            self.x = x
        self.y = 30
        self.width = 85
        self.height = 85
        self.t1 = t1
        self.t2 = t2
        self.scale = scale
        self.font = pygame.font.SysFont("monospace", 10)
        self.topeMax = 0
        self.topeMin = 0
        self.text = textfunc
        self.past = past
        self.final = final
        self.finalT = finalT
        Graphs.Array.append(self)

    def draw(self, screen, listData):
        # Se dibujan las lineas y textos de la grafica
        label = self.font.render(self.t1, 1, (0, 0, 0))
        screen.blit(label, (self.x - 15, self.y - 15))
        label = self.font.render(self.t2, 1, (0, 0, 0))
        screen.blit(label, (self.x + int((self.width / 2)), self.y + self.height + 15))
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            1,
        )
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height), 1)

        # Se dibuja cada punto en pantalla
        if Graphs.active:
            # Si esta activo se le siguen agregados datos y calculando los topes mayores
            self.past.append(listData)
            for e in self.past:
                x = int(((e[0] * self.width) / self.final) + self.x)
                y = int(((e[1] * self.height * self.scale) / self.finalT) + self.y + self.height)
                if self.topeMax == 0 or self.topeMax[0] >= y:
                    self.topeMax = [y, e[1], x, e[0]]
                if self.topeMin == 0 or self.topeMin[0] <= y:
                    self.topeMin = [y, e[1], x, e[0]]
                pygame.Surface.set_at(screen, (x, y), (0, 0, 0))
        else:
            # Si no, se dibuja directamente
            for e in self.past:
                x = int(((e[0] * self.width) / self.final) + self.x)
                y = int(((e[1] * self.height * self.scale) / self.finalT) + self.y + self.height)
                pygame.Surface.set_at(screen, (x, y), (0, 0, 0))

        self.text(self, screen)

    @classmethod
    def Clean(cls):
        Graphs.active = True
        Graphs.stopTimer = 0
        Graphs.Array = []


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


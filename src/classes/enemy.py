import pygame


from src.config import FLOOR, HEIGHT, GRAVITY


class Enemy:
    listE = []  # Lista donde se guardaran objetos caja
    destroyed = 0  # Conteo de cuantos se destruyeron en total
    falling = False  # Si hay cajas cayendo

    def __init__(self, x, y, img):
        self.image = pygame.image.load(img)
        self.x = x
        self.y = y - FLOOR
        self.width = 15
        self.height = 15
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.dibujado = True
        self.ti = (
            0  # Se creara un movimiento de caida libre con un tiempo inicial obtenido a futuro
        )
        Enemy.listE.append(self)

    def destroy(self):
        # Funcion que es llamada cuando el jugador colisiona con la caja
        if self.dibujado == True:
            self.dibujado = False
            Enemy.destroyed += 1

    def draw(self, screen):
        # Dibujado en pantalla
        if self.dibujado == True:
            screen.blit(self.image, self.rect)

    @classmethod
    def CheckCol(cls, time):
        # Funcion de colisiones entre cajas y gravedad de las mismas
        fallingCheck = 0  # Si hay cajas cayendo
        for e in range(len(Enemy.listE)):
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
            while e - multiplicador >= 0 and Enemy.listE[e - multiplicador].dibujado == False:
                # no se esta dibujando se chequea la siguiente debido a que quiere decir que el jugador impacto con la misma.
                multiplicador += 3
            if e - multiplicador >= 0:
                # Si el indice de la caja existe
                if (
                    Enemy.listE[e].rect.bottom <= Enemy.listE[e - multiplicador].rect.y
                    and Enemy.listE[e - multiplicador].rect.y - Enemy.listE[e].rect.bottom != 0
                ):
                    # Colision contra la siguiente caja
                    if Enemy.listE[e].ti == 0:
                        Enemy.listE[e].ti = time  # Se asgina el tiempo inicial
                    # Movimiento de caida libre mruv
                    Enemy.listE[e].rect.y = Enemy.listE[e].y + (GRAVITY / 2) * (
                        ((time - Enemy.listE[e].ti) / 1000.0) ** 2
                    )
                    fallingCheck += 1
            elif Enemy.listE[e].rect.bottom < HEIGHT - FLOOR:
                # Si no cae hasta tocar contra el suelo debido a que no tiene mas cajas abajo
                if Enemy.listE[e].ti == 0:
                    Enemy.listE[e].ti = time  # Se asgina el tiempo inicial
                # Movimiento de caida libre mruv
                Enemy.listE[e].rect.y = Enemy.listE[e].y + (GRAVITY / 2) * (
                    ((time - Enemy.listE[e].ti) / 1000.0) ** 2
                )
                fallingCheck += 1
        else:
            if fallingCheck > 0:
                # Si hay cajas cayendo
                Enemy.falling = True
            else:
                Enemy.falling = False

    @classmethod
    def Clean(cls):
        # Funcion que limpia los objetos cajas y resetea el estado de caida
        Enemy.falling = False
        Enemy.listE = []

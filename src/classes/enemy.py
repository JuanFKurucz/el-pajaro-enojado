import pygame


from src.config import FLOOR, HEIGHT, GRAVITY


class Enemy:
    list_objects = []  # Lista donde se guardaran objetos caja
    area_objects = [-1, -1]
    destroyed = 0  # Conteo de cuantos se destruyeron en total
    falling = False  # Si hay cajas cayendo

    def __init__(self, initial_x, initial_y, img):
        self.image = pygame.image.load(img)
        self.initial_x = initial_x
        self.initial_y = initial_y - FLOOR
        self.rect = self.image.get_rect()
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.dibujado = True
        # Se creara un movimiento de caida libre con un tiempo inicial obtenido a futuro
        self.ti = 0
        self.id = len(Enemy.list_objects)
        if Enemy.area_objects[0] == -1 or self.rect.left < Enemy.area_objects[0]:
            Enemy.area_objects[0] = self.rect.left
        if Enemy.area_objects[1] == -1 or self.rect.right > Enemy.area_objects[1]:
            Enemy.area_objects[1] = self.rect.right
        Enemy.list_objects.append(self)

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
    def get_active_enemies(cls):
        elements = [e for e in Enemy.list_objects if e.dibujado]
        elements.reverse()
        return elements

    @classmethod
    def check_collision(cls, time):
        # Funcion de colisiones entre cajas y gravedad de las mismas
        falling_check = 0  # Si hay cajas cayendo
        boxes = Enemy.get_active_enemies()
        for enemy in boxes:
            # por cada caja en la lista de cajas
            # Como las cajas estan astutamente creadas en columnas de forma
            # 			11	10	9
            # 			8	7	6
            # 			5	4	3
            # 			2	1	0
            #
            # Podemos obtener la caja que tiene abajo haciendo el indice de esta caja -3
            # Se realizo de esta forma para poder hacer real el movimiento de cada caja
            # ya que se actualiza en orden de caida
            search_box = None
            for index in range(enemy.id - 3, -1, -3):
                if Enemy.list_objects[index].dibujado:
                    search_box = Enemy.list_objects[index]
                    break
            if (search_box and search_box.rect.y > enemy.rect.bottom != 0) or (
                not search_box and enemy.rect.bottom < HEIGHT - FLOOR
            ):
                if enemy.ti == 0:
                    # Se asgina el tiempo inicial
                    # compensate for air loss
                    enemy.ti = search_box.ti if search_box and search_box.ti > 0 else time
                # Si el indice de la caja existe
                # O si no cae hasta tocar contra el suelo debido a que no tiene mas cajas abajo
                # Movimiento de caida libre mruv

                enemy.rect.y = enemy.initial_y + (GRAVITY / 2) * (((time - enemy.ti) / 1000.0) ** 2)
                falling_check += 1
        Enemy.falling = falling_check > 0

    def reset(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.dibujado = True

    @classmethod
    def Clean(cls):
        # Funcion que limpia los objetos cajas y resetea el estado de caida
        Enemy.falling = False
        for enemy in Enemy.list_objects:
            enemy.reset()

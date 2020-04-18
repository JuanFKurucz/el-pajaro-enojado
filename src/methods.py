import math


import pygame


from src.config import HEIGHT, FLOOR, GRAVITY

# Este archivo se encarga de funciones a las cuales se llamaran


def draw_text(screen, text, pos):
    # Funcion que dibuja texto en pantalla
    screen.blit(pygame.font.SysFont("monospace", 12).render(text, 1, (0, 0, 0)), pos)


def show_vars(screen, player, tf, ballXY, Enemys):
    # Funcion que muestra variables en pantalla
    start_pos = HEIGHT - FLOOR
    col0 = [
        "|F|: %s N/m" % str(round(player.fuerza, 2)),
        "Angulo: %s°" % str(round(player.angulo, 2)),
        "Tiempo Inicial: 0 s",
        "Tiempo Actual: %s s" % str(round((tf / 1000.0), 2)),
        "*Tiempo Final: %s s"
        % str(round(((player.fuerza * math.sin(math.radians(player.angulo))) * 2) / GRAVITY, 2)),
    ]
    col1 = [
        "Eje X (MRU):",
        "Velocidad Inicial: %s m/s" % str(round(player.vx, 2)),
        "Velocidad Actual: %s m/s" % str(round(player.vx, 2)),
        "Posicion Inicial: %s m" % str(round(player.x, 2)),
        "Posicion Actual: %s m" % str(round(ballXY[len(ballXY) - 1][0], 2)),
        "*Posicion Final: %s m"
        % str(
            round(
                player.x
                + (((player.fuerza * math.sin(math.radians(player.angulo))) * 2) / GRAVITY)
                * player.vx,
                2,
            )
        ),
        "Eje Y (MRUV):",
        "Velocidad Inicial: %s m/s" % str(round(player.vy, 2)),
        "Velocidad Actual: %s m/s" % str(round(player.vy - GRAVITY * (tf / 1000.0), 2)),
        "Posicion Inicial: %s m" % str(round(HEIGHT - FLOOR - player.y - player.height, 2)),
        "Posicion Actual: %s m" % str(round(ballXY[len(ballXY) - 1][1], 2)),
        "*Posicion Final: 0 m",
    ]
    col3 = [
        "Cajas Destruidas: %s" % str(player.score),
        "Cajas Destruidas Totales: %s" % str(Enemys.destroyed),
    ]
    for enum_col in enumerate(col0):
        draw_text(screen, enum_col[1], (20, 10 + start_pos + 15 * enum_col[0]))
    for enum_col in enumerate(col1):
        draw_text(
            screen,
            enum_col[1],
            (220 + 320 * (int(enum_col[0] / 6)), start_pos + 15 * ((enum_col[0]) % 6)),
        )
    for enum_col in enumerate(col3):
        draw_text(screen, enum_col[1], (10, 180 + 20 * enum_col[0]))


def text_graph_XY(self, screen):
    # Funcion que muestra datos en graficas
    texts = [
        str(round(self.topeMax[1], 2)),
        (self.x - 30, self.topeMax[0]),
        str(int((self.y + self.height) - self.topeMin[0])),
        (self.x - 2, self.topeMin[0]),
        str(round(self.topeMax[3], 2)),
        (self.topeMax[2], self.y + self.height + 8),
        str(round(self.past[len(self.past) - 1][0], 2)),
        (
            int(((self.past[len(self.past) - 1][0] * self.width) / self.final) + self.x),
            self.y + self.height,
        ),
    ]
    for t in range(0, len(texts), 2):
        draw_text(screen, texts[t], texts[t + 1])


def text_graph_T(self, screen):
    # Funcion que muestra datos en graficas
    texts = [
        str(math.fabs(round(self.topeMin[1] - self.topeMax[1], 2))),
        (self.x - 30, self.topeMax[0]),
        str(int((self.y + self.height) - self.topeMin[0])),
        (self.x - 2, self.topeMin[0]),
        str(round(self.topeMax[3] / 1000.0, 2)),
        (self.topeMax[2], self.y + self.height + 8),
        str(round(self.past[len(self.past) - 1][0] / 1000.0, 2)),
        (
            int(((self.past[len(self.past) - 1][0] * self.width) / self.final) + self.x),
            self.y + self.height,
        ),
    ]
    for t in range(0, len(texts), 2):
        draw_text(screen, texts[t], texts[t + 1])


def text_graph_TV(self, screen):
    # Funcion que muestra datos en graficas
    texts = [
        str(round(self.topeMax[1], 2) * -1),
        (self.x - 20, self.topeMax[0]),
        str(round(self.topeMin[1], 2) * -1),
        (self.x - 20, self.topeMin[0]),
    ]
    for t in range(0, len(texts), 2):
        draw_text(screen, texts[t], texts[t + 1])


def draw_handler(screen, time, player, Graphs, Enemys, background):
    # Funcion que se encarga de realizar todos los dibujos y pasarle los datos a las graficas
    background.draw(screen)  # Dibuja fondo
    player.draw(screen)  # Dibuja jugador
    for enemy in Enemys.list_objects:  # Dibuja todas las cajas
        enemy.draw(screen)

    data_graphs = [
        [
            player.rect.x,
            500 - player.rect.bottom,
        ],  # Crea todos los datos en este momento para cada grafica
        [time, -1 * player.vy + GRAVITY * (time / 1000.0)],
        [time, 500 - player.rect.bottom],
        [time, player.rect.x * -1],
    ]
    for enum_graph in enumerate(Graphs):
        # Por cada grafica, se dibuja y se le asignan los nuevos datos
        enum_graph[1].draw(screen, data_graphs[enum_graph[0]])
    show_vars(screen, player, time, Graphs[0].past, Enemys)  # Se dibuja cada variable en pantalla
    pygame.display.update()  # Se actualiza la pantalla

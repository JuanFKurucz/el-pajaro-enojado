import pygame, math


from src.config import HEIGHT, FLOOR, GRAVITY

# Este archivo se encarga de funciones a las cuales se llamaran


def drawText(screen, text, pos):
    # Funcion que dibuja texto en pantalla
    screen.blit(pygame.font.SysFont("monospace", 12).render(text, 1, (0, 0, 0)), pos)


def showVars(screen, player, tf, ballXY, Enemys):
    # Funcion que muestra variables en pantalla
    startPos = HEIGHT - FLOOR
    col0 = [
        "|F|:" + str(round(player.fuerza, 2)) + " N/m",
        "Angulo:" + str(round(player.angulo, 2)) + "°",
        "Tiempo Inicial: 0" + " s",
        "Tiempo Actual: " + str(round((tf / 1000.0), 2)) + " s",
        "*Tiempo Final:"
        + str(round(((player.fuerza * math.sin(math.radians(player.angulo))) * 2) / GRAVITY, 2))
        + " s",
    ]
    col1 = [
        "Eje X (MRU):",
        "Velocidad Inicial: " + str(round(player.vx, 2)) + " m/s",
        "Velocidad Actual: " + str(round(player.vx, 2)) + " m/s",
        "Posicion Inicial: " + str(round(player.x, 2)) + " m",
        "Posicion Actual: " + str(round(ballXY[len(ballXY) - 1][0], 2)) + " m",
        "*Posicion Final: "
        + str(
            round(
                player.x
                + (((player.fuerza * math.sin(math.radians(player.angulo))) * 2) / GRAVITY)
                * player.vx,
                2,
            )
        )
        + " m",
        "Eje Y (MRUV):",
        "Velocidad Inicial: " + str(round(player.vy, 2)) + " m/s",
        "Velocidad Actual: " + str(round(player.vy - GRAVITY * (tf / 1000.0), 2)) + " m/s",
        "Posicion Inicial: " + str(round(HEIGHT - FLOOR - player.y - player.height, 2)) + " m",
        "Posicion Actual: " + str(round(ballXY[len(ballXY) - 1][1], 2)) + " m",
        "*Posicion Final: 0 m",
    ]
    col3 = [
        "Cajas Destruidas: " + str(player.score),
        "Cajas Destruidas Totales: " + str(Enemys.destroyed),
    ]
    for c in range(len(col0)):
        drawText(screen, col0[c], (20, 10 + startPos + 15 * c))
    for c in range(len(col1)):
        drawText(screen, col1[c], (220 + 320 * (int(c / 6)), startPos + 15 * ((c) % 6)))
    for c in range(len(col3)):
        drawText(screen, col3[c], (10, 180 + 20 * c))


def textGraphXY(self, screen):
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
        drawText(screen, texts[t], texts[t + 1])


def textGraphT(self, screen):
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
        drawText(screen, texts[t], texts[t + 1])


def textGraphTV(self, screen):
    # Funcion que muestra datos en graficas
    texts = [
        str(round(self.topeMax[1], 2) * -1),
        (self.x - 20, self.topeMax[0]),
        str(round(self.topeMin[1], 2) * -1),
        (self.x - 20, self.topeMin[0]),
    ]
    for t in range(0, len(texts), 2):
        drawText(screen, texts[t], texts[t + 1])


def drawHandler(screen, time, player, Graphs, Enemys, BackGround):
    # Funcion que se encarga de realizar todos los dibujos y pasarle los datos a las graficas
    BackGround.draw(screen)  # Dibuja fondo
    player.draw(screen)  # Dibuja jugador
    for e in Enemys.listE:  # Dibuja todas las cajas
        e.draw(screen)

    dataGraphs = [
        [
            player.rect.x,
            500 - player.rect.bottom,
        ],  # Crea todos los datos en este momento para cada grafica
        [time, -1 * player.vy + GRAVITY * (time / 1000.0)],
        [time, 500 - player.rect.bottom],
        [time, player.rect.x * -1],
    ]
    for i in range(len(Graphs)):  # Por cada grafica, se dibuja y se le asignan los nuevos datos
        Graphs[i].draw(screen, dataGraphs[i])
    showVars(screen, player, time, Graphs[0].past, Enemys)  # Se dibuja cada variable en pantalla
    pygame.display.update()  # Se actualiza la pantalla

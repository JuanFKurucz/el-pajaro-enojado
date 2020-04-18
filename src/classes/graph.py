import pygame


class Graph:
    Array = []
    active = True

    def __init__(self, x, t1, t2, scale, textfunc, past, final, finalT):
        if len(Graph.Array) - 1 >= 0:
            # Si existen graficas creadas se asigna a la derecha de la misma
            self.x = (
                Graph.Array[len(Graph.Array) - 1].x + Graph.Array[len(Graph.Array) - 1].width + x
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
        Graph.Array.append(self)

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
        if Graph.active:
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
        Graph.active = True
        Graph.stopTimer = 0
        Graph.Array = []

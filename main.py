import pygame


from src.classes import BackGround, Enemy, Graph
from src.config import WIDTH, SIZE, HEIGHT
from src.game import start

# Este archivo se encarga de las funciones principales del juego

if __name__ == "__main__":
    pygame.init()  # se inicia el modulo de PyGame
    pygame.display.set_caption(
        "El pajaro enojado"
    )  # Se le agrega el titulo 'El pajaro enojado' a la ventana del juego.
    SCREEN = pygame.display.set_mode(SIZE)
    CLOCK = pygame.time.Clock()  # se declara clock para uso futuro
    while True:
        # Se especifica el ancho de la ventana como size siendo este 800,600.
        Enemy.Clean()  # Se limpia el array que guarda los enemigos en pantalla
        BackGround.Clean()  # Se limpia el array que guarda los fondos a dibujar
        Graph.Clean()  # Se limpia el array que guarda las graficas a dibujar
        # El siguiente codigo genera Enemigos, siendo estos las cajas.
        for cord_y in range(1, 20):
            for cord_x in range(5, 8):
                Enemy(WIDTH - 200 - 30 * cord_x, HEIGHT - 15 * cord_y, "./assets/box.png")
        start(SCREEN, CLOCK)  # Se llama a la funcion start pasandole las variables screen y clock

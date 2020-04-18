from src.classes import Enemy, Graph
from src.config import SIZE
from src.game import init, start

# Este archivo se encarga de las funciones principales del juego

if __name__ == "__main__":
    SCREEN, CLOCK, BACKGROUND = init(SIZE)
    while True:
        Enemy.Clean()  # Se limpia el array que guarda los enemigos en pantalla
        Graph.Clean()  # Se limpia el array que guarda las graficas a dibujar
        # El siguiente codigo genera Enemigos, siendo estos las cajas.
        start(
            SCREEN, CLOCK, BACKGROUND
        )  # Se llama a la funcion start pasandole las variables screen y clock

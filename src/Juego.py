import pygame, math, random
from OtherFunctions import *
from GameClasses import *
from Global import *
from pygame.locals import *

# Este archivo se encarga de las funciones principales del juego


def main():
    pygame.init()  # se inicia el modulo de PyGame
    screen = pygame.display.set_mode(
        size
    )  # Se especifica el ancho de la ventana como size siendo este 800,600. Variable size extraida del archivo Global.py
    pygame.display.set_caption(
        "El pajaro enojado"
    )  # Se le agrega el titulo 'El pajaro enojado' a la ventana del juego.
    Enemys.Clean()  # Se limpia el array que guarda los enemigos en pantalla
    BackGround.Clean()  # Se limpia el array que guarda los fondos a dibujar
    Graphs.Clean()  # Se limpia el array que guarda las graficas a dibujar

    # El siguiente codigo genera Enemigos, siendo estos las cajas.
    for y in range(1, 20):
        for x in range(5, 8):
            Enemys(width - 200 - 30 * x, height - 15 * y, "./assets/box.png")

    clock = pygame.time.Clock()  # se declara clock para uso futuro
    start(screen, clock)  # Se llama a la funcion start pasandole las variables screen y clock


def start(screen, clock):
    player = None  # A esta variable se le asiganara el objeto de jugador
    notTrue = True  # Control del while de tiro y resultado. Cuando es True es cuando el usuario esta asignando el angulo y fuerza. Cuando es False es cuando el jugador se esta moviendo
    lastPoint = [
        21,
        height - 21,
    ]  # Variable que guarda el ultimo punto en donde estaba el cursor, con limitaciones
    col = []  # Variable que guardara textos a imprimir en pantalla
    BackGround(0, 0, "./assets/bgi.png")  # Se crea un objeto fondo
    timeCalculated = 0  # Variable que guardara cuando demorara el tiro en caer al piso
    xfinal = 0  # Variable que guardara cual sera la posicion final en X
    ymedia = 0  # Variable que guardara cual sera la altura maxima en Y

    while notTrue == True:  # Mientras el usuario esta decidiendo Fuerza y Angulo
        # El siguiente codigo recorre los eventos del juego esperando si se pidio un evento de cierre,
        # Si este sucede se cierra el programa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.event.pump()  # se esperan mas eventos
        BackGround.draw(screen)  # Se dibuja el fondo en screen
        pygame.draw.line(
            screen, (0, 0, 0), (21, height - floor - 21), (lastPoint[0], lastPoint[1]), 4
        )  # Se dibuja la linea que va del puntero del cursor al inicio del jugador
        for c in range(len(col)):  # Para cada dato del array col
            drawText(screen, col[c], (10, 200 + 20 * c))  # Se dibuja texto en pantalla
        drawText(
            screen, Creditos, (15, 15)
        )  # Se dibuja el texto de la variable global Creditos en pantalla
        lastPoint = [
            pygame.mouse.get_pos()[0],
            pygame.mouse.get_pos()[1],
        ]  # Se asigna a lastPoint la posicion actual del cursor a traves de eventos

        if lastPoint[0] <= 21:  # Se fuerza a que la posicion menor en X sea 21
            lastPoint[0] = 21
        if (
            lastPoint[1] >= height - floor - 21
        ):  # Y se fuerza a que la posicion menor en Y sea 21 desde el piso
            lastPoint[1] = height - floor - 21

        Fuerza = round(
            math.sqrt((lastPoint[0] - 21.0) ** 2 + ((height - floor - 21.0 - lastPoint[1])) ** 2), 2
        )  # Se pitagoras para conseguir la hipotenusa de las coordenadas
        try:
            Angulo = round(
                math.degrees(
                    math.atan((height - floor - lastPoint[1] - 21.0) / (lastPoint[0] - 21.0))
                ),
                2,
            )  # Se consigue el angulo con arco tangente y/x
        except ZeroDivisionError as detail:
            Angulo = 90  # Si x es 0 se asigna al angulo 90
        timeCalculated = round(
            ((Fuerza * math.sin(math.radians(Angulo))) * 2) / g, 2
        )  # Se calcula el tiempo que va a demorar el jugador en llegar al piso
        xfinal = round(
            Fuerza * math.cos(math.radians(Angulo)) * timeCalculated, 2
        )  # Se calcula la posicion en X final
        ymedia = round(
            (timeCalculated / 2) * (Fuerza * math.sin(math.radians(Angulo)))
            + (g / 2) * ((timeCalculated / 2) ** 2) * -1,
            2,
        )  # Se calcula la altura maxima

        # Se pasan los datos anteriores a un array de textos para dibujar
        col = [
            "|F|:" + str(Fuerza) + " N/m",
            "Angulo:" + str(Angulo) + "°",
            "*Tiempo Final:" + str(timeCalculated) + " s",
            "*Posicion en X Final: " + str(xfinal) + " m",
            "*Posicion en Y Maxima: " + str(ymedia) + " m (Altura Maxima)",
        ]

        # Se dibujan los enemigos en pantalla
        for e in Enemys.listE:
            e.draw(screen)

        # Se espera el evento de clic para lanzar
        if pygame.mouse.get_pressed()[0]:
            # Una vez se hace clic se crea el jugador y se inicia el siguiente while parando a este
            player = Player("./assets/player.png", Fuerza, Angulo)
            notTrue = False
        pygame.display.update()  # Se actualiza la pantalla

    # Si alguno de los datos calculados es 0 se le asgina 1, estos datos son usados para el escalado de las graficas
    # Por ende modificarlos no afectaria a ninguna muestra en el juego visual, se asigna a 1 para que la division no de error
    if ymedia == 0:
        ymedia = 1
    pvgo = player.vy
    if player.vy == 0:
        pvgo = 1
    if xfinal == 0:
        xfinal = 1
    data1 = timeCalculated * 1000
    if data1 == 0:
        data1 = 1

    # Se crean objetos de clase Garfica
    Graphs(175, "y (m)", "x (m)", -1, textGraphXY, [[0, 0]], xfinal, ymedia)
    Graphs(45, "Vy", "t (s)", 1, textGraphTV, [], data1, pvgo)
    Graphs(45, "y (m) ", "t (s)", -1, textGraphT, [[0, 0]], data1, ymedia)
    Graphs(45, "x (m) ", "t (s)", 1, textGraphT, [[0, 0]], data1, xfinal)

    startTick = (
        pygame.time.get_ticks()
    )  # Se consigue el tiempo inicial del juego, ya que el tiempo empieza a incrementarse una vez que se inicia el juego.
    BackGround(0, 0, "./assets/bg.png")  # Se crea el nuevo fondo
    updateTime = (
        True  # Esta variable controlara si hay que seguir escribiendo el aumento del tiempo
    )
    elapsed = 0  # Esta variable tendra lo que demoro en ejecutar el codigo
    while notTrue == False:
        seconds = elapsed  # Se asigna lo que se demoro en ejecutar el codigo al dato de la ultima linea de este while
        if (
            pygame.time.get_ticks() - startTick
        ) - seconds >= 0:  # Si este delay no hace ser al tiempo negativo
            time = (
                pygame.time.get_ticks() - startTick
            ) - seconds  # Se hace el calculo de tiempo real, es decir el tiempo actual menos el tiempo inicial.
        else:
            time = (
                pygame.time.get_ticks() - startTick
            )  # Para prevenir errores si la resta da negativo porque se demoro en entrar al codigo se evita hacer eso

        # Se esperan eventos de cierre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break
        pygame.event.pump()
        if pygame.mouse.get_pressed()[2]:  # Si el usuario hace clic derecho se termina el while
            break

        if (
            player.rect.bottom < height - floor or time < 100
        ):  # Si la parte de abajo del jugador es menor que la altura del piso, siendo q el Y se incrementa hacia abajo
            # Normalmente esto seria si la parte de abajo del jugador es mayor al piso
            player.rect.y = (
                player.y - player.vy * (time / 1000.0) + (g / 2) * ((time / 1000.0) ** 2)
            )  # Se realiza el movimiento con la Ley Horaria de MURV en Y
            if (
                player.rect.left >= 0 or player.rect.right <= width
            ):  # Si el jugador se encuentra dentro de la pantalla en X
                player.rect.x = player.x + player.vx * (
                    time / 1000.0
                )  # Se mueve al jugador en X con MRU
        elif updateTime == True:  # Si el jugador se da contra el piso
            Graphs.active = False  # Se dejan de agregar valores a las graficas
            updateTime = time  # Se deja de actualizar el tiempo

        if Enemys.falling == True or (
            player.rect.bottom > 0
            and player.rect.right >= Enemys.listE[len(Enemys.listE) - 1].rect.left
            and player.rect.left <= Enemys.listE[0].rect.right
        ):  # Si hay enemigos cayendo o el jugador esta en el area de enemigos
            Enemys.CheckCol(time)  # Se comprueba colisiones y caidas de enemigos
            player.CheckCol(Enemys.listE)  # Se comprueban colisiones de jugador con enemigos

        if updateTime == True:  # Si se tiene que actualizar el tiempo en variables
            drawHandler(
                screen, time, player, Graphs.Array, Enemys, BackGround
            )  # Se da el tiempo normal
        else:
            drawHandler(
                screen, updateTime, player, Graphs.Array, Enemys, BackGround
            )  # Si no se da el guardado cuando el jugador se da contra el piso
        elapsed = clock.tick(
            120
        )  # Se asigna el maximo de FPS a 120 y esta variable es la que de la diferencia
    main()  # Una vez haga clic derecho el juego se reiniciara llamando a main


if __name__ == "__main__":
    main()
input("ok")

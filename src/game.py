import math


import pygame


from src.methods import drawText, textGraphXY, textGraphT, textGraphTV, drawHandler
from src.classes import BackGround, Enemy, Graph, Player
from src.config import WIDTH, HEIGHT, FLOOR, CREDITS, GRAVITY


def check_close():
    # Se esperan eventos de cierre
    # El siguiente codigo recorre los eventos del juego esperando
    # si se pidio un evento de cierre,
    # Si este sucede se cierra el programa
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.event.pump()  # se esperan mas eventos


def init(SIZE):
    pygame.init()
    pygame.display.set_caption("El pajaro enojado")

    # Crear enemigos
    for cord_y in range(1, 20):
        for cord_x in range(5, 8):
            Enemy(WIDTH - 200 - 30 * cord_x, HEIGHT - 15 * cord_y, "./assets/box.png")
    return pygame.display.set_mode(SIZE), pygame.time.Clock(), BackGround(0, 0)


def start(screen, clock, background):
    player = None

    last_cursor_position = [
        21,
        HEIGHT - 21,
    ]
    time_calculated = 0  # Variable que guardara cuando demorara el tiro en caer al piso
    xfinal = 0  # Variable que guardara cual sera la posicion final en X
    ymedia = 0  # Variable que guardara cual sera la altura maxima en Y
    background.set_image("./assets/bgi.png")
    while True:  # Mientras el usuario esta decidiendo strength y angle
        check_close()

        player_y = HEIGHT - FLOOR - 21

        background.draw(screen)  # Se dibuja el fondo en screen
        # Se dibuja la linea que va del puntero del cursor al inicio del jugador
        pygame.draw.line(
            screen, (0, 0, 0), (21, player_y), (last_cursor_position[0], last_cursor_position[1]), 4
        )

        # Se dibuja el texto de la variable global Creditos en pantalla
        drawText(screen, CREDITS, (15, 15))

        # Se asigna a last_cursor_position la posicion actual del cursor a traves de eventos
        last_cursor_position = [
            pygame.mouse.get_pos()[0] if pygame.mouse.get_pos()[0] > 21 else 21,
            pygame.mouse.get_pos()[1] if pygame.mouse.get_pos()[1] < player_y else player_y,
        ]

        strength = round(
            math.sqrt(
                (last_cursor_position[0] - 21.0) ** 2 + ((player_y - last_cursor_position[1])) ** 2
            ),
            2,
        )  # Se pitagoras para conseguir la hipotenusa de las coordenadas
        try:
            angle = round(
                math.degrees(
                    math.atan(
                        (player_y - last_cursor_position[1]) / (last_cursor_position[0] - 21.0)
                    )
                ),
                2,
            )  # Se consigue el angulo con arco tangente y/x
        except ZeroDivisionError:
            angle = 90  # Si x es 0 se asigna al angulo 90
        # Se calcula el tiempo que va a demorar el jugador en llegar al piso
        formula_1 = strength * math.sin(math.radians(angle))
        time_calculated = round((formula_1 * 2) / GRAVITY, 2)
        # Se calcula la posicion en X final
        xfinal = round(strength * math.cos(math.radians(angle)) * time_calculated, 2)
        # Se calcula la altura maxima
        ymedia = round(
            (time_calculated / 2) * formula_1 + (GRAVITY / 2) * ((time_calculated / 2) ** 2) * -1,
            2,
        )

        # Se dibujan los enemigos en pantalla
        for enemy in Enemy.list_objects:
            enemy.draw(screen)

        for row in enumerate(
            [
                "|F|: %s N/m" % str(strength),
                "angle: %s°" % str(angle),
                "*Tiempo Final: %s s" % str(time_calculated),
                "*Posicion en X Final: %s m" % str(xfinal),
                "*Posicion en Y Maxima: %s m (Altura Maxima)" % str(ymedia),
            ]
        ):
            drawText(screen, row[1], (10, 200 + 20 * row[0]))  # Se dibuja texto en pantalla

        # Se espera el evento de clic para lanzar
        if pygame.mouse.get_pressed()[0]:
            # Una vez se hace clic se crea el jugador y se inicia el siguiente while parando a este
            player = Player("./assets/player.png", strength, angle)
            break
        pygame.display.update()  # Se actualiza la pantalla

    # Si alguno de los datos calculados es 0 se le asgina 1, estos datos
    # son usados para el escalado de las graficas
    # Por ende modificarlos no afectaria a ninguna muestra en el juego visual,
    # se asigna a 1 para que la division no de error
    if ymedia == 0:
        ymedia = 1
    pvgo = player.vy
    if player.vy == 0:
        pvgo = 1
    if xfinal == 0:
        xfinal = 1
    data1 = time_calculated * 1000
    if data1 == 0:
        data1 = 1

    # Se crean objetos de clase Garfica
    Graph(175, "y (m)", "x (m)", -1, textGraphXY, [[0, 0]], xfinal, ymedia)
    Graph(45, "Vy", "t (s)", 1, textGraphTV, [], data1, pvgo)
    Graph(45, "y (m) ", "t (s)", -1, textGraphT, [[0, 0]], data1, ymedia)
    Graph(45, "x (m) ", "t (s)", 1, textGraphT, [[0, 0]], data1, xfinal)

    # Se consigue el tiempo inicial del juego, ya que el tiempo
    # empieza a incrementarse una vez que se inicia el juego.
    start_tick = pygame.time.get_ticks()

    background.set_image("./assets/bg.png")

    # Esta variable controlara si hay que seguir escribiendo el aumento del tiempo
    update_time = True

    elapsed = 0  # Esta variable tendra lo que demoro en ejecutar el codigo
    half_gravity = GRAVITY / 2
    while True:
        # Se asigna lo que se demoro en ejecutar el codigo al dato de la ultima linea de este while
        calculated_value = pygame.time.get_ticks() - start_tick
        time = calculated_value if calculated_value - elapsed < 0 else calculated_value - elapsed

        check_close()
        if pygame.mouse.get_pressed()[2]:  # Si el usuario hace clic derecho se termina el while
            break

        if player.rect.bottom < HEIGHT - FLOOR or time < 100:
            # Si la parte de abajo del jugador es menor que la altura del piso,
            # siendo q el Y se incrementa hacia abajo
            # Normalmente esto seria si la parte de abajo del jugador es mayor al piso
            # Se realiza el movimiento con la Ley Horaria de MURV en Y
            time_ms = time / 1000.0
            player.rect.y = player.y - player.vy * time_ms + half_gravity * (time_ms ** 2)
            if player.rect.left >= 0 or player.rect.right <= WIDTH:
                # Si el jugador se encuentra dentro de la pantalla en X
                # Se mueve al jugador en X con MRU
                player.rect.x = player.x + player.vx * time_ms
        elif update_time:
            # Si el jugador se da contra el piso
            Graph.active = False  # Se dejan de agregar valores a las graficas
            update_time = time  # Se deja de actualizar el tiempo

        if Enemy.falling or (
            player.rect.bottom > 0
            and player.rect.right >= Enemy.list_objects[len(Enemy.list_objects) - 1].rect.left
            and player.rect.left <= Enemy.list_objects[0].rect.right
        ):
            # Si hay enemigos cayendo o el jugador esta en el area de enemigos
            Enemy.CheckCol(time)  # Se comprueba colisiones y caidas de enemigos
            player.CheckCol(Enemy.list_objects)  # Se comprueban colisiones de jugador con enemigos

        if update_time:  # Si se tiene que actualizar el tiempo en variables
            # Se da el tiempo normal
            drawHandler(screen, time, player, Graph.Array, Enemy, background)
        else:
            # Si no se da el guardado cuando el jugador se da contra el piso
            drawHandler(screen, update_time, player, Graph.Array, Enemy, background)
        # Se asigna el maximo de FPS a 120 y esta variable es la que de la diferencia
        elapsed = clock.tick(120)

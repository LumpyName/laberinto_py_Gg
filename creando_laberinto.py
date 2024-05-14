from os import system
from main import Laberinto, Jugador
from time import sleep
from pprint import pprint
import random

def movimiento(jugador):
    # Retornar una tupla dentro de una lista [(x, y), (x, y)]
    # el valor de cada tupla son coordenadas que el jugador puede
    # realisar y si retorna una lista vacia se quedo sin movimientos
    movimientos = {
            "above": (-1, 0),
            "below": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
    }
    coor = lambda new_move: (movimientos[new_move][0], movimientos[new_move][1])
    old_x, old_y = jugador.eje_x, jugador.eje_y
    list_return = []
    for move in movimientos.keys():
        if laberinto.is_trapped(move):
            dx, dy = coor(move)
            list_return.append((old_x + dx, old_y + dy))
    return list_return



salir = False
while salir == False:
    jugador = Jugador("☺", 21, 2, "Andres")
    laberinto = Laberinto(jugador)
    
    while True:
        system("clear")
        print(laberinto)
        movimientos = movimiento(jugador)
        if len(movimientos) == 0:
            break
        new_x, new_y = random.choice(movimientos.copy())
        laberinto.actualizar(new_x, new_y)
        var_1 = jugador.eje_x == 1
        var_2 = jugador.eje_y == 59
        if var_1 and var_2:
            salir = True
    sleep(1)

print(laberinto)

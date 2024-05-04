from pprint import pprint
from pynput import keyboard
from os import system

class Laberinto:
    _chr_sp = ['╚', '╝', '╔', '╗', '╩', '╦', '╠', '╣', '═', '╬', '║']

    def __init__(self, jugador):
        self.jugador = jugador
        self._mapa = self._generar_mapa()
        self.juego_terminado = False

    def _generar_mapa(self):
        mapa = [[' ' for _ in range(60)] for _ in range(23)]
        mapa[0] = ['╔'] + ['═' for _ in range(58)] + ['╗']
        mapa[1] = ['║'] + [' ' for _ in range(58)] + [' ']
        for x in range(2, 21):
            mapa[x] = ['║'] + [' ' for _ in range(58)] + ['║']
        mapa[-2] = list('╚   ') + ['═' for _ in range(55)] + ['╝']
        mapa[-1] = list('  Start')
        mapa[self.jugador.eje_x][self.jugador.eje_y] = self.jugador.cuerpo_jugador
        return mapa

    def move(self, direccion):
        movimientos = {
            "above": (-1, 0),
            "below": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        dx, dy = movimientos[direccion]
        x, y = self.jugador.eje_x + dx, self.jugador.eje_y + dy
        if direccion in ["above", "below"]:
            v_y = (1, -1) if direccion == "above" else (1, -1)
            if 0 <= x < 22 and 0 <= y < 60 and self._mapa[x][y + v_y[0]] == self._mapa[x][y + v_y[1]] == " ":
                self._mapa[x][y] = self._mapa[self.jugador.eje_x][self.jugador.eje_y]
                self._mapa[self.jugador.eje_x][self.jugador.eje_y] = " "
                self.jugador.eje_x, self.jugador.eje_y = x, y
        elif direccion in ["left", "right"]:
            try:
                if 0 <= x < 22 and 0 <= y < 60 and self._mapa[self.jugador.eje_x][y] == " " and self._mapa[self.jugador.eje_x][y + (1 if direccion == "right" else -1)] == " ":
                    self._mapa[self.jugador.eje_x][y] = self._mapa[self.jugador.eje_x][self.jugador.eje_y]
                    self._mapa[self.jugador.eje_x][self.jugador.eje_y] = " "
                    self.jugador.eje_y = y
            except IndexError:
                self.juego_terminado = True
        
    def __str__(self):
        return '\n'.join([''.join(fila) for fila in self._mapa])


class Jugador:
    def __init__(self, cuerpo_jugador, eje_x, eje_y, nombre="Player"):
        self.cuerpo_jugador = cuerpo_jugador
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.nombre = "(" + nombre + ")"

    def probando(self):
        print("Sep se realiza cambios en tiempo real")

jugador = Jugador('☺', 21, 2, "Lumpy")
laberinto = Laberinto(jugador)
system("clear")
print(laberinto)

def on_key_press(key):
    key = str(key)
    match key:
        case "Key.up":
            laberinto.move("above")
        case "Key.down":
            laberinto.move("below")
        case "Key.right":
            laberinto.move("right")
        case "Key.left":
            laberinto.move("left")
        case "'q'":
            return False
    if laberinto.juego_terminado:
        system("clear")
        for _ in range(9):
            print()
        print("      ____                            _          ")
        print("     / ___|  __ _  _ __    __ _  ___ | |_   ___  ")
        print("    | |  _  / _` || '_ \  / _` |/ __|| __| / _ \ ")
        print("    | |_| || (_| || | | || (_| |\__ \| |_ |  __/ ")
        print("     \____| \__,_||_| |_| \__,_||___/ \__| \___| ")
        print()
        print(jugador.nombre.center(44))
        for _ in range(8):
            print()
        return False
    else:
        system("clear")
        print(laberinto)

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

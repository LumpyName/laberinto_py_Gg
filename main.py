from pprint import pprint
from pynput import keyboard
from os import system

class Laberinto:
    _chr_sp = ['╚', '╝', '╔', '╗', '╩', '╦', '╠', '╣', '═', '╬', '║']

    def __init__(self, jugador):
        self.jugador = jugador
        mapa = [[' ' for _ in range(60)] for _ in range(23)]
        mapa[0] = ['╔'] + ['═' for _ in range(58)] + ['╗']
        mapa[1] = ['║'] + [' ' for _ in range(58)] + [' ']
        for x in range(2, 21):
            mapa[x] = ['║'] + [' ' for _ in range(58)] + ['║']
        mapa[-2] = list('╚   ') + ['═' for _ in range(55)] + ['╝']
        mapa[-1] = list('  Start')
        mapa[self.jugador.eje_x][self.jugador.eje_y] = self.jugador.cuerpo_jugador
        self._mapa = mapa

    def moveAndTrack(self, direccion, track=' '):
        movimientos = {
            "above": (-1, 0),
            "below": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        dx, dy = movimientos[direccion]
        old_x, old_y = self.jugador.eje_x, self.jugador.eje_y
        new_x, new_y = old_x + dx, old_y + dy
        cuerpo_jugador = self.jugador.cuerpo_jugador

        def realizarMovimiento():
            # Realizando el movimiento...
            self._mapa[old_x][old_y] = track
            self._mapa[new_x][new_y] = cuerpo_jugador

            # Guardando posicion del jugador
            self.jugador.eje_x = new_x
            self.jugador.eje_y = new_y

        if direccion in ["above", "below"]:
            if self.is_trapped(direccion):
                realizarMovimiento()

        elif direccion in ["left", "right"]:
            if self.is_trapped(direccion):
                realizarMovimiento()
            else:
                self._ganador(direccion)

    def _ganador(self, direccion):
        cuerpo_jugador = self.jugador.cuerpo_jugador
        if direccion == "right":
            coor = (self.jugador.eje_x, self.jugador.eje_y)
            if coor == (1, 58):
                self._mapa[coor[0]][coor[1]] = ' '
                self._mapa[coor[0]][coor[1] + 1] = cuerpo_jugador
                self.juego_terminado = True

    def is_trapped(self, side):
        # Se obtiene la ubicacion del cuerpo del jugador
        dx, dy = self.jugador.eje_x, self.jugador.eje_y

        # Verificar si tiene para ir a la derecha
        if side == "right":
            var_1 = self._mapa[dx][dy + 1: dy + 3]
            return var_1 == [" "] * 2

        # Verificar si tiene para ir a la izquierda
        elif side == "left":
            var_1 = self._mapa[dx][dy - 2: dy]
            return var_1 == [" "] * 2

        # Verificar si tiene para ir a la arriba
        elif side == "above":
            for x in range(dy - 1, dy + 2):
                if self._mapa[dx - 1][x] != " ":
                    break
            else:
                return True

        # Verificar si tiene para ir a la abajo
        elif side == "below":
            for x in range(dy - 1, dy + 2):
                if self._mapa[dx + 1][x] != " ":
                    break
            else:
                return True

    # Es una herramienta que nos servira mas tarde
    def actualizar(self, new_x, new_y):
        old_x, old_y = self.jugador.eje_x, self.jugador.eje_y
        self._mapa[old_x][old_y] = "#"
        self._mapa[new_x][new_y] = self.jugador.cuerpo_jugador
        if self._mapa[1][59] == self.jugador.cuerpo_jugador:
            self.jugador.juego_terminado = True
        self.jugador.eje_x = new_x
        self.jugador.eje_y = new_y

        return False

    def getMapa(self):
        return self._mapa
    
    def __str__(self):
        return '\n'.join([''.join(fila) for fila in self._mapa])


class Jugador:
    def __init__(self, cuerpo_jugador, eje_x, eje_y, nombre="Player"):
        self.cuerpo_jugador = cuerpo_jugador
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.nombre = nombre
        self.juego_terminado = False

    def get_position(self):
        return (self.eje_x, self.eje_y)

def on_key_press(key):
    key = str(key)
    match key:
        case "Key.up":
            laberinto.moveAndTrack("above")
        case "Key.down":
            laberinto.moveAndTrack("below")
        case "Key.right":
            laberinto.moveAndTrack("right")
        case "Key.left":
            laberinto.moveAndTrack("left")
        case "'q'":
            return False
    if jugador.juego_terminado:
        return False
    else:
        system("clear")
        print(laberinto)

def get_print_ganador(mapa):
    texts = [
        list("   ____                            _          "),
        list("  / ___|  __ _  _ __    __ _  ___ | |_   ___  "),
        list(" | |  _  / _` || '_ \  / _` |/ __|| __| / _ \ "),
        list(" | |_| || (_| || | | || (_| |\__ \| |_ |  __/ "),
        list("  \____| \__,_||_| |_| \__,_||___/ \__| \___| "),
        list(f" ╔{'═'*(len(jugador.nombre) + 2)}╗ "),
        list(f" ║ {jugador.nombre} ║ "),
        list(f" ╚{'═'*(len(jugador.nombre) + 2)}╝ ")
    ]
    indice_inicio = len(mapa) // 2 - (len(texts)) // 2

    for num, line in enumerate(texts):
        var_1 = indice_inicio + num
        indice_linea = len(mapa[var_1]) // 2 - (len(line)) // 2
        mapa[var_1][indice_linea : indice_linea + len(line)] = line

    return mapa

if __name__ == "__main__":
    jugador = Jugador('☺', 21, 2, "Lumpy")
    laberinto = Laberinto(jugador)
    system("clear")
    print(laberinto)
    
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

    # Para imprimir un buen mensaje de que gano
    system("clear")
    print_mapa = get_print_ganador(laberinto.getMapa())
    print("\n".join(["".join(fila) for fila in print_mapa]))

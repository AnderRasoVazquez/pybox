# -*- coding: utf-8 -*-
"""Este modulo se encarga de lanzar el programa."""

# TODO ver si existe el token (configparser)
    # TODO si no existe coger y guardar el token
    # TODO si existe leer el token
    # TODO (maybe) multiplatform

from .command_line import CmdInterpreter


def main():
    """Funcion principal."""
    client = CmdInterpreter()
    client.cmdloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nPrograma interrumpido.'
        exit(1)


# -*- coding: utf-8 -*-
"""Este modulo se encarga de lanzar el programa."""

# TODO ver si existe el token (configparser)
    # TODO si no existe coger y guardar el token
    # TODO si existe leer el token
    # TODO (maybe) multiplatform

from .parser import Parser


def main():
    """Funcion principal."""
    Parser().parse_args()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nPrograma interrumpido.'
        exit(1)


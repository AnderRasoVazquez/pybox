# -*- coding: utf-8 -*-
"""Este modulo se encarga de lanzar el programa."""

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


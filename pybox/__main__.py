# -*- coding: utf-8 -*-

# TODO ver si existe el token (configparser)
    # TODO si no existe coger y guardar el token
    # TODO si existe leer el token
    # TODO (maybe) multiplatform

from .client import DropboxClient


def main():
    """Funcion principal."""
    client = DropboxClient()
    client.cmdloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nPrograma interrumpido.'
        exit(1)


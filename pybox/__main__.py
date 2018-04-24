# -*- coding: utf-8 -*-

# TODO ver si existe el token (configparser)
    # TODO si no existe coger y guardar el token
    # TODO si existe leer el token
    # TODO (maybe) multiplatform

# TODO argparse para elegir si descargar compartir o lo que sea

# TODO subir un archivo
# TODO descargar un archivo
# TODO borrar un archivo
# TODO compartir un archivo

from .client import DropboxClient


client = DropboxClient()


client.run()



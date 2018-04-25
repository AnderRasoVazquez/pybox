# -*- coding: utf-8 -*-
"""Este modulo se encarga de gestionar los metadatos."""


class File(object):
    """Representa un archivo o una carpeta de dropbox."""
    def __init__(self, the_id, the_type, name, path_display, path_lower):
        self.id = the_id
        self.type = the_type
        self.name = name
        self.path_display = path_display
        self.path_lower = path_lower

    def __str__(self):
        if self.is_folder():
            return self.name + "/"
        else:
            return self.name

    def is_file(self):
        """Devuelve True si es un archivo."""
        return self.type == "file"

    def is_folder(self):
        """Devuelve True si es una carpeta."""
        return self.type == "folder"

    def get_full_path(self):
        """Devuelve la ruta del archivo."""
        return self.path_display

# -*- coding: utf-8 -*-


class File(object):
    """Representa un archivo o carpeta de dropbox."""
    def __init__(self, id, type, name, path_display, path_lower):
        self.id = id
        self.type = type
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
        return self.path_display


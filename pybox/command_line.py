# -*- coding: utf-8 -*-
"""Este modulo se encarga de gestionar los comandos en un interprete de terminal."""

import os.path

from os import listdir
from os.path import isfile, join
from cmd import Cmd

from .metadata import File
from .dropbox_client import DropboxClient


FORECOLORS = {
    "black": '\x1b[30m',
    "red": '\x1b[31m',
    "green": '\x1b[32m',
    "yellow": '\x1b[33m',
    "blue": '\x1b[34m',
    "magenta": '\x1b[35m',
    "cyan": '\x1b[36m',
    "white": '\x1b[37m',
    "bold": '\033[1m',
    "none": '\x1b[39m'
}

BACKCOLORS = {
    "black": '\x1b[40m',
    "red": '\x1b[41m',
    "green": '\x1b[42m',
    "yellow": '\x1b[43m',
    "blue": '\x1b[44m',
    "magenta": '\x1b[45m',
    "cyan": '\x1b[46m',
    "white": '\x1b[47m',
    "none": '\x1b[49m'
}

RESETSTYLE = '\x1b[0m'

LS_FOLDER = FORECOLORS['bold'] + FORECOLORS['blue'] + BACKCOLORS['none']
LS_FILE = FORECOLORS['none'] + BACKCOLORS['none']
DOLLAR = FORECOLORS['bold'] + FORECOLORS['green'] + BACKCOLORS['none']
BRACKETS = FORECOLORS['bold'] + FORECOLORS['red'] + BACKCOLORS['none']
PATH = FORECOLORS['bold'] + FORECOLORS['cyan'] + BACKCOLORS['none']


class CmdInterpreter(object, Cmd):
    """Cliente para comunicarse con Dropbox."""

    def __init__(self):
        Cmd.__init__(self)
        self.client = DropboxClient()
        self.files = []
        self.folder = "/"
        self._construct_tree(self.client.get_tree(self.folder))
        self.prompt_intro = "dropbox:"
        self.prompt = ""
        self.current_folder = "/"
        self.intro = "Iniciando cliente de dropbox..."
        self.color = True
        self._update_prompt()

    def _update_prompt(self):
        """Actualiza el prompt de la terminal."""
        if self.color:
            self.prompt = BRACKETS + "[" + PATH + self.prompt_intro + self.current_folder + BRACKETS + "]" + DOLLAR + "$ " + RESETSTYLE
        else:
            self.prompt = "[" + self.prompt_intro + self.current_folder + "]$ "

    def postcmd(self, stop, line):
        """Funcion que se ejecuta sola despues de ejecutar cada comando."""
        self._update_prompt()

    def _construct_tree(self, tree):
        """Construye el arbol de carpetas de la ubicacion actual."""
        for item in tree["entries"]:
            the_file = File(item["id"], item[".tag"], item["name"],
                            item["path_display"], item["path_lower"])
            self.files.append(the_file)

    def _update_tree(self, folder):
        """Actualiza el arbol de carpetas con el de la carpeta indicada."""
        self._empty_tree()
        self._construct_tree(self.client.get_tree(folder))
        self.folder = os.path.dirname(os.path.dirname(folder))

    def _go_back(self):
        """Va hacia atras una carpeta."""
        self._empty_tree()
        self._construct_tree(self.client.get_tree(self.folder))
        self.current_folder = self.folder
        self.folder = os.path.dirname(self.folder)

    def _empty_tree(self):
        """Vacia la informacion del arbol de carpetas."""
        self.files = []

    def _show_tree(self):
        """Muestra la informacion del arbol de carpetas."""
        index = 0
        for element in self.files:
            index += 1
            if element.is_folder() and self.color:
                print LS_FOLDER + str(element) + RESETSTYLE
            else:
                print str(element)

    def update_folder_content(self):
        """Actualiza el arbol de carpetas para buscar cambios nuevos."""
        self._update_tree(self.current_folder)

    def _get_completions(self, text):
        """Devuelve el contenido del arbol de la carpeta actual para hacer autocompletado."""
        return [i.name for i in self.files if i.name.startswith(text)]

    def _get_file_completions(self, text):
        """Devuelve el contenido del arbol de la carpeta actual para hacer autocompletado si es un archivo."""
        return [i.name for i in self.files if i.is_file() and i.name.startswith(text)]

    def _get_folder_completions(self, text):
        """Devuelve el contenido del arbol de la carpeta actual para hacer autocompletado si es un archivo."""
        return [i.name for i in self.files if i.is_folder() and i.name.startswith(text)]

    def do_ls(self, arg):
        """Representa el comando ls."""
        self._show_tree()

    def help_ls(self):
        """Muestra la ayuda del comando ls."""
        print "Muestra el contenido de la carpeta actual."

    def do_pwd(self, arg):
        """Representa el comando pwd."""
        print self.current_folder

    def help_pwd(self):
        """Muestra la ayuda del comando pwd."""
        print "Muestra la ruta de la carpeta actual."

    def do_cd(self, arg):
        """Representa el comando cd."""
        if arg in ["..", "../"]:
            self._go_back()
        elif arg:
            item_path = self.current_folder + arg
            if item_path[-1] != "/":
                item_path += "/"
            try:
                self._update_tree(item_path)
                self.current_folder = item_path
            except:
                self._update_tree(self.current_folder)
        else:
            self.current_folder = "/"
            self._update_tree("/")

    def complete_cd(self, text, line, begidx, endidx):
        """Autocompletado para el comando cd."""
        return self._get_folder_completions(text)

    def help_cd(self):
        """Muestra la ayuda del comando cd"""
        print "Entra dentro de la carpeta indicada."

    def _get_file(self, file_name):
        """Devuelve el archivo indicado si existe, si no None."""
        file_found = False
        for item in self.files:
            if item.name == file_name:
                return item
        return None

    def do_rm(self, arg):
        """Representa el comando rm."""
        if self._get_file(arg):
            try:
                self.client.rm(self.current_folder + arg)
                self.update_folder_content()
            except:
                print "Error al intentar eliminar el archivo."
        else:
            print "El archivo a eliminar no existe.."

    def help_rm(self):
        """Muestra la ayuda del comando rm."""
        print "Eliminar un archivo o carpeta."

    def complete_rm(self, text, line, begidx, endidx):
        """Autocompletado para el comando rm."""
        return self._get_completions(text)

    def _get_file_id(self, file_name):
        """Devuelve el id del archivo indicado."""
        for item in self.files:
            if file_name == item.name:
                return item.id
        raise Exception("El archivo indicado no existe.")

    def do_share(self, arg):
        """Representa el comando share."""
        if self._get_file(arg):
            try:
                mail = raw_input("Compartir con: ")
                file_id = self._get_file_id(arg)
                self.client.share_file_by_id(arg, file_id, mail)
            except:
                print "Error al intentar compartir el archivo."
        else:
            print "El archivo a compartir no existe."

    def help_share(self):
        """Muestra la ayuda del comando share."""
        print "Compartir un archivo."

    def complete_share(self, text, line, begidx, endidx):
        """Autocompletado para el comando share."""
        return self._get_file_completions(text)

    def do_download(self, arg):
        """Representa el comando download."""
        item = self._get_file(arg)
        if item:
            try:
                if item.is_folder():
                    self.client.download_folder(self.current_folder + arg)
                else:
                    self.client.download_file(self.current_folder + arg)
            except:
                print "Error al intentar descargar el archivo."
        else:
            print "El archivo a descargar no existe.."

    def help_download(self):
        """Muestra la ayuda del comando download."""
        print "Descargar un archivo o carpeta."

    def complete_download(self, text, line, begidx, endidx):
        """Autocompletado para el comando download."""
        return self._get_completions(text)

    def do_upload(self, arg):
        """Representa el comando upload."""
        mypath = os.getcwd()
        if arg not in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
            print "Archivo '" + arg + "' no encontrado en la carpeta '" + mypath + "'."
        else:
            self.client.upload(arg, self.current_folder)
            self.update_folder_content()

    def help_upload(self):
        """Muestra la ayuda del comando upload."""
        print "Subir un archivo."

    def complete_upload(self, text, line, begidx, endidx):
        """Autocompletado para el comando upload."""
        mypath = os.getcwd()
        return [f for f in listdir(mypath) if isfile(join(mypath, f)) if f.startswith(text)]

    def do_color(self, arg):
        """Representa el comando que activa o desactiva el color."""
        self.color = not self.color

    def help_color(self):
        """Muestra la ayuda del comando color."""
        print "Activa o desactiva los colores."

    def do_update(self, arg):
        """Representa el comando update."""
        self.update_folder_content()

    def help_update(self):
        """Muestra la ayuda del comando update."""
        print "Actualiza el contenido de la carpeta."

    def do_exit(self, s):
        """Representa el comando para salir del programa."""
        exit(0)

    def help_exit(self):
        """Muestra la ayuda del comando exit."""
        print "Salir del programa."
        print "Tambien puedes usar el atajo Ctrl-D."

    # Para manejar el atajo Ctrl-D
    do_EOF = do_exit
    help_EOF = help_exit


import requests
import json

from cmd import Cmd

from .metadata import File

import os.path

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

class DropboxClient(object, Cmd):
    """Cliente para comunicarse con Dropbox."""

    def __init__(self):
        # TODO conseguir el token
        Cmd.__init__(self)
        self.token = "4PUJzfSzG6AAAAAAAAABnBKIkgGOIkS88n9OP9TnJGLMtR0R4Xl3mYrHvI1FWqaD"
        self.files = []
        self.folder = "/"
        self._construct_tree(self._get_tree(self.folder))
        self.prompt_intro = "dropbox:"
        self.prompt = ""
        self.current_folder = "/"
        self.intro = "Iniciando cliente de dropbox..."
        self.color = True
        self._update_prompt()

    def _update_prompt(self):
        if self.color:
            self.prompt = BRACKETS + "[" + PATH + self.prompt_intro + self.current_folder + BRACKETS + "]" + DOLLAR + "$ " + RESETSTYLE
        else:
            self.prompt = "[" + self.prompt_intro + self.current_folder + "]$ "

    def postcmd(self, stop, line):
        self._update_prompt()

    def _get_tree(self, folder=""):
        """Devuelve un diccionario con los contenidos de la carpeta."""
        if folder == "/":
            folder = ""

        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

        data = {"path": folder}

        response = requests.post('https://api.dropboxapi.com/2/files/list_folder', headers=headers, json=data)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise Exception("Folder name didn't return any result.")

    def _construct_tree(self, tree):
        for item in tree["entries"]:
            the_file = File(item["id"], item[".tag"], item["name"],
                            item["path_display"], item["path_lower"])
            self.files.append(the_file)

    def _update_tree(self, folder):
        self._empty_tree()
        self._construct_tree(self._get_tree(folder))
        self.folder = os.path.dirname(os.path.dirname(folder))

    def _go_back(self):
        self._empty_tree()
        self._construct_tree(self._get_tree(self.folder))
        self.current_folder = self.folder
        self.folder = os.path.dirname(self.folder)

    def _empty_tree(self):
        self.files = []

    def _select_item(self, item_number):
        """Elegir el elemento de la lista."""
        # TODO hacer comprobaciones de que el numero es correcto
        if 0 <= item_number < len(self.files):
            if item_number == 0:
                self._go_back()
            else:
                item_number -= 1
                item = self.files[item_number]
                if item.is_folder():
                    item_path = item.get_full_path()
                    self.current_folder = item_path
                    self._update_tree(item_path)
                else:
                    print "is file, todavia sin implementar"
        else:
            print "Not valid number, try again."

    def _show_interface(self):
        index = 0
        for element in self.files:
            index += 1
            if element.is_folder() and self.color:
                print LS_FOLDER + str(element) + RESETSTYLE
            else:
                print str(element)

    def run(self):
        while True:
            self._show_interface()
            option = raw_input("\nInsert number and press ENTER ('q' to quit):\n")
            # TODO repetir hasta que sea correcto el numero o q
            print "\n\n\n\n"
            if option == "q":
                exit()
            self._select_item(int(option))

    def _get_completions(self, text):
        return [i.name for i in self.files if i.name.startswith(text)]

    def do_ls(self, arg):
        self._show_interface()

    def help_ls(self):
        print "Muestra el contenido de la carpeta actual."

    def do_pwd(self, arg):
        print self.current_folder

    def help_pwd(self):
        print "Mustra la ruta de la carpeta actual."

    def do_cd(self, arg):
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
        return [i.name for i in self.files if i.is_folder() and i.name.startswith(text)]
        # return [i for i in self.files if i.is_folder() and i.startswith(text)]

    def help_cd(self):
        print "Entra dentro de la carpeta indicada."

    def do_debug(self, arg):
        print "self.current_folder " + self.current_folder
        print "self.folder " + self.folder

    def do_rm(self, arg):
        print "remove sin implementar a", arg

    def help_rm(self):
        print "Eliminar un archivo o carpeta."

    def complete_rm(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def do_share(self, arg):
        print "Compartir un archivo o carpeta", arg

    def help_share(self):
        print "Compartir un archivo o carpeta."

    def complete_share(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def do_download(self, arg):
        print "Descargar un archivo o carpeta", arg

    def help_download(self):
        print "Descargar un archivo o carpeta."

    def complete_download(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def do_upload(self, arg):
        print "Subir un archivo o carpeta", arg

    def help_upload(self):
        print "Subir un archivo o carpeta."

    def complete_upload(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def do_color(self, arg):
        self.color = not self.color

    def help_color(self):
        print "Activa o desactiva los colores."

    def do_exit(self, s):
        exit(0)

    def help_exit(self):
        print "Salir del programa."
        print "Tambien puedes usar el atajo Ctrl-D."

    # Para manejar el atajo Ctrl-D
    do_EOF = do_exit
    help_EOF = help_exit


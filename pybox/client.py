# -*- coding: utf-8 -*-

import requests
import json
import os.path

from os import listdir
from os.path import isfile, join
from cmd import Cmd

from .metadata import File


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

    def _show_interface(self):
        index = 0
        for element in self.files:
            index += 1
            if element.is_folder() and self.color:
                print LS_FOLDER + str(element) + RESETSTYLE
            else:
                print str(element)

    def update_folder_content(self):
        self._update_tree(self.current_folder)

    def _get_completions(self, text):
        return [i.name for i in self.files if i.name.startswith(text)]

    def _get_file_completions(self, text):
        return [i.name for i in self.files if i.is_file() and i.name.startswith(text)]

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

    def help_cd(self):
        print "Entra dentro de la carpeta indicada."

    def do_debug(self, arg):
        print "self.current_folder " + self.current_folder
        print "self.folder " + self.folder

    def rm(self, item_path):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

        data = {"path": item_path}

        response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', headers=headers, json=data)

        if response.status_code == 200:
            print "Eliminado: '" + item_path + "'"
        else:
            print response
            print response.content
            raise Exception("Remove didn't return any result.")
        pass

    def do_rm(self, arg):
        file_found = False
        for item in self.files:
            if item.name == arg:
                file_found = True
                try:
                    self.rm(self.current_folder + arg)
                    self.update_folder_content()
                except:
                    print "Error al intentar eliminar el archivo."
                break
        if not file_found:
            print "El archivo a eliminar no existe.."

    def help_rm(self):
        print "Eliminar un archivo o carpeta."

    def complete_rm(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def _get_file_id(self, file_name):
        for item in self.files:
            if file_name == item.name:
                return item.id
        raise Exception("El archivo indicado no existe.")

    def share_file(self, file_name, mail):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

        file_id = self._get_file_id(file_name)

        data = {
            "file": file_id,
            "members": [
                {
                    ".tag": "email",
                    "email": mail
                }
            ],
            "access_level": "viewer",
        }

        response = requests.post('https://api.dropboxapi.com/2/sharing/add_file_member', headers=headers, json=data)

        if response.status_code == 200:
            print "Compartido: '" + self.current_folder + file_name + "'"
        else:
            print response
            print response.content
            raise Exception("Error while sharing file.")
        pass

    def do_share(self, arg):
        file_found = False
        for item in self.files:
            if item.name == arg and item.is_file():
                file_found = True
                try:
                    mail = raw_input("Share with: ")
                    self.share_file(arg, mail)
                except:
                    print "Error al intentar compartir el archivo."
                break
        if not file_found:
            print "El archivo a compartir no existe."

    def help_share(self):
        print "Compartir un archivo."

    def complete_share(self, text, line, begidx, endidx):
        return self._get_file_completions(text)

    def download_file(self, file_path):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": '{"path": ' + '"' + file_path + '"' + '}'
        }

        response = requests.post('https://content.dropboxapi.com/2/files/download', headers=headers)

        if response.status_code == 200:
            filename = file_path.split('/')[-1]
            open(filename, 'wb').write(response.content)
            print "Descargado: '" + filename + "'"
        else:
            raise Exception("Download didn't return any result.")

    def download_folder(self, file_path):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": self._format_json([("path", file_path)])
        }

        response = requests.post('https://content.dropboxapi.com/2/files/download_zip', headers=headers)

        if response.status_code == 200:
            filename = file_path.split('/')[-1]
            filename += ".zip"
            open(filename, 'wb').write(response.content)
            print "Descargado: '" + filename + "'"
        else:
            raise Exception("Download didn't return any result.")

    def do_download(self, arg):
        file_found = False
        for item in self.files:
            if item.name == arg:
                file_found = True
                try:
                    if item.is_folder():
                        self.download_folder(self.current_folder + arg)
                    else:
                        self.download_file(self.current_folder + arg)
                except:
                    print "Error al intentar descargar el archivo."
                break
        if not file_found:
            print "El archivo a descargar no existe.."

    def help_download(self):
        print "Descargar un archivo o carpeta."

    def complete_download(self, text, line, begidx, endidx):
        return self._get_completions(text)

    def _format_json_key(self, key, value):
        if value.lower() not in ["true", "false"]:
            return '"%s": "%s"' % (key, value)
        else:
            return '"%s": %s' % (key, value)


    def _format_json(self, the_list):
        result = "{"
        index = 0
        size = len(the_list)
        while index < size:
            result += self._format_json_key(the_list[index][0], the_list[index][1])
            if index != size - 1:
                result += ", "
            index += 1
        result += "}"
        return result

    def upload(self, file_path):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": self._format_json([("path", self.current_folder + file_path), ("mode", "add"), ("autorename", "true"), ("mute", "false")]),
            "Content-Type": "application/octet-stream"
        }

        # - -data - binary @ local_file.txt
        the_file = open(file_path, 'rb')
        files = {'file': the_file}
        try:
            response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, files=files)
        finally:
            the_file.close()

        if response.status_code == 200:
            print "Subido: '" + file_path + "'"
        else:
            raise Exception("Error during download.")
        pass

    def do_upload(self, arg):
        mypath = os.getcwd()
        if arg not in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
            print "Archivo '" + arg + "' no encontrado en la carpeta '" + mypath + "'."
        else:
            self.upload(arg)
            self.update_folder_content()

    def help_upload(self):
        print "Subir un archivo."

    def complete_upload(self, text, line, begidx, endidx):
        mypath = os.getcwd()
        return [f for f in listdir(mypath) if isfile(join(mypath, f)) if f.startswith(text)]

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

    def do_update(self, arg):
        self.update_folder_content()

    def help_update(self):
        print "Actualiza el contenido de la carpeta."


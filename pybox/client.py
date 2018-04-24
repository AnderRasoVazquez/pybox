import requests
import json

from .metadata import File

import os.path


class DropboxClient(object):
    """Cliente para comunicarse con Dropbox."""
    def __init__(self):
        # TODO conseguir el token
        self.token = "4PUJzfSzG6AAAAAAAAABnBKIkgGOIkS88n9OP9TnJGLMtR0R4Xl3mYrHvI1FWqaD"
        self.files = []
        self.folder = "/"
        self._construct_tree(self._get_tree(self.folder))
        self.current_folder = "/"

    def _get_tree(self, folder=""):
        """Devuelve un diccionario con los contenidos de la carpeta."""
        if folder == "/":
            folder = ""
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

        data = {
            "path": folder,
            # "path": "",
            # "recursive": False
            # "include_media_info": False,
            # "include_deleted": False,
            # "include_has_explicit_shared_members": False,
            # "include_mounted_folders": False
        }

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
        # TODO update folder
        self._empty_tree()
        self.folder = os.path.dirname(folder)
        self._construct_tree(self._get_tree(folder))

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
        print "-----------------------"
        print self.current_folder
        print "-----------------------"
        sep = " | "
        index = 0
        if self.current_folder != "/":
            print str(index) + sep + "../"
        for file in self.files:
            index += 1
            print str(index) + sep + str(file)
        print "-----------------------"

    def run(self):
        while True:
            self._show_interface()
            option = raw_input("\nInsert number and press ENTER ('q' to quit):\n")
            # TODO repetir hasta que sea correcto el numero o q
            print "\n\n\n\n"
            if option == "q":
                exit()
            self._select_item(int(option))

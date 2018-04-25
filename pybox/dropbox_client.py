# -*- coding: utf-8 -*-
"""Este modulo se encarga de realizar operaciones en Dropbox."""

import requests
import json

from .utils import format_json


class DropboxClient(object):
    """Esta clase representa un cliente de dropbox."""
    def __init__(self, token):
        self.token = token

    def get_tree(self, folder=""):
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

    def rm(self, item_path):
        """Elimina un archivo o una carpeta."""
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

    def share_file(self, file_name, file_id, mail):
        """Comparte un archivo."""
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }

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
            print "Compartido: '" + file_name + "'"
        else:
            print response
            print response.content
            raise Exception("Error while sharing file.")
        pass

    def download_file(self, file_path):
        """Descarga un archivo."""
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
        """Descarga una carpeta."""
        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": format_json([("path", file_path)])
        }

        response = requests.post('https://content.dropboxapi.com/2/files/download_zip', headers=headers)

        if response.status_code == 200:
            filename = file_path.split('/')[-1]
            filename += ".zip"
            open(filename, 'wb').write(response.content)
            print "Descargado: '" + filename + "'"
        else:
            raise Exception("Download didn't return any result.")

    def upload(self, file_path, current_folder):
        """Sube un archivo."""
        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": format_json([("path", current_folder + file_path),
                                            ("mode", "add"), ("autorename", "true"), ("mute", "false")]),
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

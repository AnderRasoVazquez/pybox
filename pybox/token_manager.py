# -*- coding: utf-8 -*-
"""Este modulo se encarga de gestionar el token."""


import socket
import urllib
import webbrowser
import json
import requests
import os.path


class TokenManager(object):
    """Esta clase se encarga de descargar, guardar o mostrar el token."""
    def __init__(self):
        self.port = 8586
        self.token_path = os.path.dirname(os.path.abspath(__file__)) + '/data/token'
        self.client_id = "7veypz9j473hv46"
        self.client_secret = '8frtxz74m0ur5uc'
        self.token = self._get_token()

    def _get_code(self):
        """Obtiene el codigo."""
        server = 'www.dropbox.com'
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:' + str(self.port)
        }

        params_encoded = urllib.urlencode(params)
        resource = '/1/oauth2/authorize?' + params_encoded

        uri = 'https://' + server + resource
        webbrowser.open_new(uri)

        print 'Petición al usuario de Autenticación y Permiso...'

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(('localhost', self.port))
        listen_socket.listen(1)

        print 'Serving HTTP on port %s ...' % self.port

        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)

        print "Conexion local Respuesta:"
        print request

        http_response = """\
        HTTP/1.1 200 OK
        <html>
        <head><title>Prueba </title></head>
        <body>
        The authentication flow has completed. Close this window.
        </body>
        </html>
        """
        client_connection.sendall(http_response)
        client_connection.close()

        code = request.split('\n')[0].split('?')[1].split('=')[1].split(' ')[0]
        return code

    def _obtain_token(self, code):
        """Obtiene el token online."""
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'http://localhost:' + str(self.port)
        }

        headers = {
            'User-Agent':'Python Client',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post('https://api.dropboxapi.com/1/oauth2/token', headers=headers, data=data)

        if response.status_code == 200:
            return json.loads(response.content)["access_token"]
        else:
            print response
            print response.content
            raise Exception("Couldn't retrieve access token.")

    def _save_token(self, token):
        """Guarda el token."""
        path = os.path.dirname(os.path.abspath(__file__)) + '/data/token'
        with open(path, 'w') as f:
            f.write(token)

    def _get_token(self):
        """Obtiene el token."""
        saved_token = self._read_token()
        if saved_token:
            return saved_token
        else:
            code = self._get_code()
            token = self._obtain_token(code)
            self._save_token(token)
            return token

    def _read_token(self):
        """Lee el token guardado."""
        if os.path.isfile(self.token_path):
            with open(self.token_path, 'r') as f:
                return f.read()
        return None


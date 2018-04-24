# -*- coding: utf-8 -*-

import socket
import urllib
import webbrowser
import json
import requests

PORT = 8586

def get_token():
    ######################################################################################
    # CODE: Abrir en el navegador la URI
    # https://www.dropbox.com//oauth2/authorize
    ######################################################################################
    servidor = 'www.dropbox.com'
    params = {'response_type': 'code',
    'client_id': "7veypz9j473hv46",
              # 'redirect_uri': 'http://localhost'}
    'redirect_uri': 'http://localhost:' + str(PORT)}
    # 'redirect_uri': 'http://127.0.0.1:8586'}

    params_encoded = urllib.urlencode(params)
    recurso = '/1/oauth2/authorize?' + params_encoded

    uri = 'https://' + servidor + recurso
    print uri
    webbrowser.open_new(uri)


    print '###############################################################################'
    print 'Petición al usuario de Autenticación y Permiso: Devuelve el Code'
    print '###############################################################################'
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('localhost', PORT))
    listen_socket.listen(1)
    print 'Serving HTTP on port %s ...' % PORT
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
    print "code:"+ code


    ######################################################################################
    # ACCESS_TOKEN: Obtener el TOKEN
    # https://www.api.dropboxapi.com/1/oauth2/token
    #####################################################################################
    parametros = {'code': code,
                  'grant_type': 'authorization_code',
                  'client_id': '7veypz9j473hv46',
                  'client_secret': '8frtxz74m0ur5uc',
                  'redirect_uri': 'http://localhost:' + str(PORT)}

    cabeceras = {'User-Agent':'Python Client',
                'Content-Type': 'application/x-www-form-urlencoded'}

    respuesta = requests.post('https://api.dropboxapi.com/1/oauth2/token', headers=cabeceras,
                              data=parametros)

    print respuesta.status_code
    json_respuesta = json.loads(respuesta.content)

    access_token = json_respuesta['access_token']
    print "Access_Token:" + access_token

    # • Objetivo es desarrollar un cliente de línea de comandos de Dropbox.
    # – Daremos la posibilidad al usuario de subir, descargar, borrar y
    # compartir un fichero de dropbox
    # – La autenticación y autorización del usuario se realizara por medio
    # OAuth 2.0.
    # – Mientras el access token sea válido no se debe realizar de nuevo el
    # proceso de autenticación


def get_tree(filename=""):
    cabeceras = {
        "Authorization": "Bearer 4PUJzfSzG6AAAAAAAAABnBKIkgGOIkS88n9OP9TnJGLMtR0R4Xl3mYrHvI1FWqaD",
        "Content-Type": "application/json"
    }


    parametros = {
        "path": filename,
        # "path": "",
        # "recursive": False
        # "include_media_info": False,
        # "include_deleted": False,
        # "include_has_explicit_shared_members": False,
        # "include_mounted_folders": False
    }


    print cabeceras
    print parametros
    respuesta = requests.post('https://api.dropboxapi.com/2/files/list_folder', headers=cabeceras, json=parametros)

    print respuesta
    print respuesta.content
    files = json.loads(respuesta.content)

    for item in files["entries"]:
        print item[".tag"], item["name"]

get_tree()

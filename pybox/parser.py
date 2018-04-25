# -*- coding: utf-8 -*-
"""Este modulo se encarga de parsear el input del programa."""

import argparse

from .command_line import CmdInterpreter
from .dropbox_client import DropboxClient


class Parser(object):
    """Se encarga de parsear el input."""
    def __init__(self):
        self._parser = self._build_parser()
        self.client = DropboxClient()

    def _build_parser(self):
        """Construye el parser."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='commands', dest='command')

        parser_rm = subparsers.add_parser('rm', help='removes a file')
        parser_rm.add_argument('file_path',
                               type=str,
                               help='file path')

        parser_share = subparsers.add_parser('share', help='Share a file')
        parser_share.add_argument('file_path',
                                  type=str,
                                  help='file path')
        parser_share.add_argument('email',
                                  type=str,
                                  help='Share with email.')

        parser_upload = subparsers.add_parser('upload', help='Upload a file')
        parser_upload.add_argument('file_path',
                                   type=str,
                                   help='file path')
        parser_upload.add_argument('destination',
                                   type=str,
                                   help='Dropbox folder destination.')

        parser_download = subparsers.add_parser('download', help='rm a file')
        parser_download.add_argument('file_path',
                                     type=str,
                                     help='file path')
        parser_download.add_argument('local_destination',
                                     type=str,
                                     default=None,
                                     nargs="?",
                                     help='Where to download.')

        parser_terminal = subparsers.add_parser('terminal', help='Open an interactive terminal')

        return parser

    def test_parser(self, test_args=None):
        """Test parser."""
        args = self._parser.parse_args(args=test_args)
        return args

    def parse_args(self):
        """Parsea los argumentos."""
        args = self._parser.parse_args()
        if args.command == "share":
            self.share(args)
        elif args.command == "terminal":
            self.terminal(args)
        elif args.command == "upload":
            self.upload(args)
        elif args.command == "download":
            self.download(args)
        elif args.command == "rm":
            self.rm(args)

    def terminal(self, args):
        """Abre una terminal interactiva."""
        CmdInterpreter().cmdloop()

    def upload(self, args):
        """Sube un archivo."""
        try:
            self.client.upload(args.file_path, args.destination)
        except:
            print "Error al subir el fichero."
            exit(1)

    def rm(self, args):
        """Elimina un archivo."""
        try:
            self.client.rm(args.file_path)
        except:
            print "Error al eliminar el fichero."
            exit(1)

    def download(self, args):
        """Descarga un archivo, si no se indica donde lo descargara donde es haya ejecutado el programa."""
        try:
            self.client.download_file(args.file_path, args.local_destination)
        except:
            print "Error al descargar el fichero."
            exit(1)

    def share(self, args):
        """Comparte un archivo."""
        try:
            self.client.share_file_by_path(args.file_path, args.email)
        except:
            print "Error al compartir el fichero."
            exit(1)



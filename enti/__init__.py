# -*- coding: utf-8 -*-

from enti.version import __version__
from flask_cors import CORS
from enti.settings import AppConfig
from enti.extensions import socketio, celery, log

class Server():

    def __init__(self):
        """
        Initializes the Flask Application
        """

        if AppConfig.ROLE == 'ui':

            log.info(
                "            _   _   \n"
                "  ___ _ __ | |_(_)  \n"
                " / _ \ '_ \| __| |  External Entity Manager\n"
                "|  __/ | | | |_| |  Version v{}\n"
                " \___|_| |_|\__|_|  Digital Reasoning\n"
                "                   ".format(__version__)
            )

            from enti.ui.app import create_app
            self.app = create_app(AppConfig)
            CORS(self.app)

            log.info('Application set to run SocketIO server')
        else:


            self.app = celery
            log.info('Application set to run Celery server')

    def run(self):
        """
        Runs the Socket.IO Web Server
        """
        socketio.run(self.app,
                     host=AppConfig.SERVER_HOST,
                     port=int(AppConfig.SERVER_PORT))

app = Server().app

if __name__ == '__main__':
    Server().run()

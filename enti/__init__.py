# -*- coding: utf-8 -*-

from enti.version import __version__
from flask_cors import CORS
from enti.settings import AppConfig
from enti.extensions import socketio, celery, log
from enti.database import init_db

class Server():

    def __init__(self):
        """
        Initializes the Flask Application
        """

        if AppConfig.ROLE == 'ui':

            log.info(
                "\n"
                "            _   _   \n"
                "  ___ _ __ | |_(_)  \n"
                " / _ \ '_ \| __| |  External Entity Manager\n"
                "|  __/ | | | |_| |  Version v{}\n"
                " \___|_| |_|\__|_|  Digital Reasoning\n"
                "                   ".format(__version__)
            )

            from enti.ui.conf import create_app
            self.app = create_app(AppConfig)
            CORS(self.app)

            init_db()
            log.info('Server initialization complete')
        else:

            self.app = celery
            log.info('Server initialization complete')

    def run(self):
        """
        Runs the Socket.IO Web Server
        """
        socketio.run(self.app,
                     host=AppConfig.SERVER_HOST,
                     port=int(AppConfig.SERVER_PORT),
                     use_reloader=True)

app = Server().app

if __name__ == '__main__':
    Server().run()

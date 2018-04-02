# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from enti.settings import AppConfig
from enti.extensions import bcrypt, socketio, cors


def create_app(config=None):

    def register_extensions(app):
        """
        Initialize application extensions

        :param app: Flask application
        :return: None
        """
        with app.app_context():
            cors.init_app(app)
            bcrypt.init_app(app)
            socketio.init_app(app)

    def register_blueprints(app):
        """
        Register application views

        :param app: Flask application
        :return: None
        """
        from enti.ui.views.main import blueprint
        app.register_blueprint(blueprint)

    def register_error_handlers(app):
        """
        Register error page views

        :param app: Flask application
        :return: None
        """

        def render_error(error):
            """
            Render error pages from corresponding HTML templates

            :param error: Error code
            :return: HTML page
            """
            error_code = getattr(error, 'code', 500)
            return render_template("{0}.html".format(error_code)), error_code

        for errcode in [401, 404, 500]:
            app.errorhandler(errcode)(render_error)
        return None

    # Initialize the Flask application
    app = Flask(__name__)

    # Configure the Flask application from a given configuration
    if config is None:
        config = AppConfig
    app.config.from_object(config)

    # Register application components
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app

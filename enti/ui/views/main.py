# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template
)
from flask_socketio import emit

from enti.controller import Controller
from enti.extensions import log, socketio
from flask import jsonify, Response
import json

blueprint = Blueprint('main', __name__, url_prefix=None, static_folder="../static", static_url_path="/static")

controller = Controller()


@blueprint.route('/')
def home():
    """
    Render the index page

    :return: index.html
    """
    log.info("Accessed route: index")
    return render_template('index.html')

@blueprint.route('/initialize')
def initialize():
    """
    Initialize the site
    :return: JSON Response
    """
    try:
        log.info('Starting initialization')
        controller.initialize()
        log.info('Initialization complete')
        return Response(json.dumps({'status':'OK'}), status=200, mimetype='application/json')

    except Exception as e:
        log.exception(e)
        log.error('Initialization failed')
        return Response(json.dumps({'status': 'ERROR', 'cause':str(e)}), status=500, mimetype='application/json')

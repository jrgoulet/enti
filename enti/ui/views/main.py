# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template
)
from flask_socketio import emit

from enti.controller import Controller
from enti.extensions import log, socketio

blueprint = Blueprint('main', __name__, url_prefix=None, static_folder="../static", static_url_path="/static")

atc = Controller()


@blueprint.route('/')
def home():
    """
    Render the index page

    :return: index.html
    """
    log.info("Accessed route: index")
    return render_template('index.html')

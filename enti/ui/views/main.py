# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template
)
from flask_socketio import emit

from enti.controller import Controller
from enti.extensions import log, socketio
from flask import jsonify, Response, request
from werkzeug.utils import secure_filename
import json
from enti.settings import FileConfig
import os


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



@blueprint.route('/upload', methods=['POST'])
def upload():

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() == 'xml'

    if 'file' not in request.files:
        log.error('No file in request')
    file = request.files['file']

    if file.filename == '':
        log.error('No filename in the request')
        return Response(json.dumps({'status': 'Fail'}), status=400, mimetype='application/json')

    if not allowed_file(file.filename):
        log.error('File type not allowed')
        return Response(json.dumps({'status': 'Fail'}), status=400, mimetype='application/json')


    log.info('Saving file')
    filename = secure_filename(file.filename)
    file.save(os.path.join(FileConfig.DATA_DIR, filename))
    log.info('File saved successfully')
    return Response(json.dumps({'status': 'Success'}), status=200, mimetype='application/json')



@socketio.on('attribute.sync', namespace='/')
def sync_attributes(null):

    emit('attribute.sync', controller.sync_attributes())

@socketio.on('xml.upload', namespace='/')
def upload_xml(null):

    controller.upload_xml()


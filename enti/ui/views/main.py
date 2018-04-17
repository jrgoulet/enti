# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template
)
from flask_socketio import emit

from enti.controller import Controller
from enti.extensions import log, socketio
from flask import jsonify, Response, request, send_file
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

@blueprint.route('/export', methods=['GET'])
def download(data=None):
    return send_file(FileConfig.EXPORT_FILE, attachment_filename='entities.xml', as_attachment=True)

@socketio.on('attribute.sync', namespace='/')
def sync_attributes(null):
    emit('attribute.sync', controller.sync_attributes())

@socketio.on('entity.sync.all', namespace='/')
def sync_attributes(null):
    emit('entity.sync.all', controller.sync_entities())

@socketio.on('entity.type.sync', namespace='/')
def sync_entity_types(null):
    emit('entity.type.sync', controller.sync_entity_types())

@socketio.on('entity.add', namespace='/')
def add_entity(data):
    log.info('Adding entity', extra=data)

    try:
        entity_id = controller.add_entity(data)
        emit('entity.sync', controller.sync_entity(entity_id))
        emit('entity.add.success', None)
    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})
        emit('entity.add.failure', None)

@socketio.on('entity.remove', namespace='/')
def remove_entity(data):
    log.info('Removing entity', extra=data)

    entity_id = data.get('id')

    try:
        controller.remove_entity(entity_id)
        emit('info', {'title': 'Remove Entity', 'message': 'Entity removed successfully'})
    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('xml.upload', namespace='/')
def upload_xml(null):
    controller.upload_xml()
    emit('entity.sync.all', controller.sync_entities())

@socketio.on('attribute.update', namespace='/')
def update_attribute(data):
    log.info('Updating attribute', extra=data)

    entity_id = data.get('entityId')
    field_id = data.get('fieldId')
    value = data.get('value')

    if value is None or len(value) == 0:

        emit('danger', {'title':'Invalid Request', 'message': 'The field cannot be empty. Please try again'})

    else:
        try:
            controller.update_attribute(field_id, value)
            emit('entity.sync', controller.sync_entity(entity_id))

        except Exception as e:
            emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('attribute.remove', namespace='/')
def remove_attribute(data):

    log.info('Removing attribute', extra=data)

    entity_id = data.get('entityId')
    attribute_id = data.get('attributeId')

    try:
        controller.remove_attribute(attribute_id)
        emit('entity.sync', controller.sync_entity(entity_id))

    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('attribute.add', namespace='/')
def add_attribute(data):

    log.info('Adding attribute', extra=data)

    entity_id = data.get('entityId')
    attribute_id = data.get('attributeId')
    fields = data.get('fields')

    try:
        controller.add_attribute(entity_id, attribute_id, fields)
        emit('entity.sync', controller.sync_entity(entity_id))

    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('entity.update', namespace='/')
def update_entity(data):

    log.info('Updating entity', extra=data)

    entity_id = data.get('id')

    try:
        controller.update_entity(entity_id, data)
        emit('entity.sync', controller.sync_entity(entity_id))

    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('entity.export.all', namespace='/')
def export_entities(null):

    log.info('Exporting entities')

    try:
        controller.export_entities()
        emit('entity.export.all.success', None)

    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('synic.sync', namespace='/')
def sync_synic(data=None):
    log.info('Synchronizing Synic API')

    try:
        emit('synic.sync', controller.sync_synic())

    except Exception as e:
        emit('synic.sync.fail', None)
        emit('danger', {'title': 'Error', 'message': str(e)})

@socketio.on('synic.ingest', namespace='/')
def sync_synic(data):

    log.info('Sending entities to Synthesys for ingestion')

    try:
        kg_name = data.get('kg')

        if kg_name is None:
            raise Exception('Knowledge graph cannot be null')

        emit('synic.ingest.success', controller.ingest_entities(kg_name))

    except Exception as e:
        emit('danger', {'title': 'Error', 'message': str(e)})
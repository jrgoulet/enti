# -*- coding: utf-8 -*-

from enti.database import session_scope
from enti.extensions import celery, log
from enti.definitions import AttributeTypes, EntityTypes, ArityTypes, AttributeFields
from enti.utils.parser import load_yml
from enti.settings import FileConfig
from enti.models import Attribute, LinkedAttributeField
from enti.query import Query


@celery.task()
def initialize_defaults():
    with session_scope() as session:
        for defaults in AttributeTypes.list(), EntityTypes.list(), ArityTypes.list(), AttributeFields.list():
            for default in defaults:
                def_type = type(default)
                try:
                    def_existing = session.query(def_type).get(default.id)

                    if def_existing is None:
                        log.debug('Initializing default {}: {}'.format(def_type.__name__, default.name))
                        session.add(default)
                    else:
                        log.debug('Entry exists for {}: {}'.format(def_type.__name__, default.name))
                except Exception as e:
                    log.error('Failed to add default {}: {} due to: {}'.format(def_type.__name__, default.name, str(e)))
                    session.rollback()


def initialize_attributes():
    log.debug('Initializing attributes')

    with session_scope() as session:
        attr_templates = load_yml(FileConfig.ATTR_SCHEMA_FILE)

        for attr_id, attr_template in attr_templates.items():
            try:
                attribute = Attribute(id=attr_id,
                                      name=attr_template['name'],
                                      required=attr_template.get('required', False),
                                      arity=attr_template['arity'],
                                      ko_name=attr_template['ko_name'],
                                      description=attr_template['description'],
                                      type=attr_template['type'])
                attribute_existing = Query.Attribute.get(session, attr_id)

                if attribute_existing is None:
                    log.debug('Initializing attribute: {}'.format(attribute.name))
                    session.add(attribute)

                else:
                    log.debug('Attribute exists, skipping: {}'.format(attribute.name))

                for field_id in attr_template['fields']:
                    attr_field = Query.AttributeField.get(session, field_id)

                    if attr_field is not None:
                        linked_attr_field = LinkedAttributeField(attribute.id, attr_field.id)
                        linked_attr_field_existing = Query.LinkedAttributeField.get(session, linked_attr_field.id)

                        if linked_attr_field_existing is None:
                            log.debug('Creating linked attribute field {} for attribute {}'.format(attr_field.name,
                                                                                                  attribute.name))
                            session.add(linked_attr_field)
                    else:
                        log.error('Attribute field {} is not defined in field definitions. Please add field to '
                                  'enumeration located in definitions.py. Skipping for now.'.format(field_id))
            except Exception as e:
                log.error('Failed to initialize attribute: {} due to: {}'.format(attr_id, str(e)))

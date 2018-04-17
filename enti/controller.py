from enti.tasks import import_entities
from enti.query import Query
from enti.database import session_scope
from enti.settings import FileConfig, AppConfig
from enti.utils.parser import run_entity_extraction, export_entity_xml
import os
from enti.extensions import log
from enti.models import EntityAttribute, EntityAttributeField, Entity
from enti.synthesys import SynicAPI
from datetime import datetime
from pprint import pprint
from enti.utils.time import get_elapsed_minutes


class Controller:

    def __init__(self):
        self.last_ingestion_ts = None

    def initialize(self):
        pass

    def sync_attributes(self):

        with session_scope() as session:
            attr_json = {a.id: a.json() for a in Query.Attribute.all(session)}

            for attr_id in attr_json.keys():
                linked_fields = {
                    lf.field_id: Query.AttributeField.get(session, lf.field_id).json()
                    for lf in Query.LinkedAttributeField.filter(session, attr_id)
                }

                attr_json[attr_id]['fields'] = linked_fields

            return attr_json

    def sync_entity_types(self):

        with session_scope() as session:
            type_json = {t.id: t.json() for t in Query.EntityType.all(session)}

            return type_json

    def sync_arity_types(self):

        with session_scope() as session:
            arity_json = {a.id: a.json() for a in Query.ArityType.all(session)}

            return arity_json

    def update_attribute(self, field_id, value):

        with session_scope() as session:

            field = Query.EntityAttributeField.get(session, field_id)

            if field is None:

                raise Exception('Entity Attribute Field not found')

            else:

                old_val = field.value
                log.info('Updating field {} value from {} to {}'.format(field_id, old_val, value))

                field.value = value

    def export_entities(self):

        entity_json = self.sync_entities()
        export_entity_xml(entity_json)

    def add_entity(self, data):

        with session_scope() as session:

            entity_id = data.get('id')

            if entity_id is None or len(entity_id) == 0:
                raise Exception('Entity ID cannot be empty.')

            if Query.Entity.get(session, entity_id) != None:
                raise Exception('Entity ID is already in use.')

            name = data.get('name')

            if name is None or len(name) == 0:
                raise Exception('Entity Name cannot be empty.')

            _type = data.get('type')
            entity_type = Query.EntityType.get(session, _type)
            if entity_type is None:
                raise Exception('Entity type {} is not recognized as a valid type.'.format(_type))

            canonical = data.get('canonical')
            if canonical not in ('true', 'false', True, False):
                raise Exception('Canonical value must be a boolean value (true, false).')
            if isinstance(canonical, str):
                canonical = canonical.lower() == 'true'

            entity = Entity(name=name, type=_type, canonical=canonical, id=entity_id)
            session.add(entity)

            return entity_id

    def remove_entity(self, entity_id):

        with session_scope() as session:
            entity = Query.Entity.get(session, entity_id)
            attributes = Query.EntityAttribute.filter(session, entity_id)
            for attribute in attributes:
                session.delete(attribute)
            session.delete(entity)

    def update_entity(self, entity_id, data):

        with session_scope() as session:
            entity = Query.Entity.get(session, entity_id)
            if entity is None:
                raise Exception('Could not locate entity identified by ID: {}'.format(entity_id))

            name = data.get('name')
            if name is None or len(name) == 0:
                raise Exception('Entity name cannot be left empty. Please enter a value.')
            entity.name = name

            _type = data.get('type')
            entity_type = Query.EntityType.get(session, _type)
            if entity_type is None:
                raise Exception('Entity type {} is not recognized as a valid type.'.format(_type))
            entity.type = _type

            canonical = data.get('canonical')
            if canonical not in ('true', 'false', True, False):
                raise Exception('Canonical value must be a boolean value (true, false).')
            if isinstance(canonical, str):
                canonical = canonical.lower() == 'true'
            entity.canonical = canonical

    def remove_attribute(self, attribute_id):

        with session_scope() as session:
            attribute = Query.EntityAttribute.get(session, attribute_id)
            fields = Query.EntityAttributeField.filter(session, attribute_id)

            for field in fields:
                session.delete(field)

            session.delete(attribute)

    def add_attribute(self, entity_id, attribute_id, fields):

        with session_scope() as session:

            attr = Query.Attribute.get(session, attribute_id)

            existing_entity_attrs = Query.EntityAttribute.filter(session, entity_id=entity_id,
                                                                 attribute_id=attribute_id)
            if attr.arity_id.lower() == "one":

                if len(existing_entity_attrs) > 0:
                    raise Exception('Arity restriction on attribute {} is preventing the addition of another value. To'
                                    ' continue, please modify or remove the existing entry for this attribute.'.format(
                        attribute_id))

            attribute = EntityAttribute(entity_id, attribute_id)
            session.add(attribute)
            session.commit()

            for existing_attr in existing_entity_attrs:
                matches = 0

                for field_id, value in fields.items():
                    lf = Query.LinkedAttributeField.filter(session, attribute_id, field_id)
                    if lf is not None:
                        existing_field = Query.EntityAttributeField.filter(session, entity_attribute_id=existing_attr.id, linked_field_id=lf.id)

                        if existing_field is not None:

                            if existing_field.value == value:
                                matches += 1
                    else:
                        raise Exception('Field {} not linked to attribute {}'.format(field_id, attribute_id))

                if matches == len(fields.keys()):
                    raise Exception('Duplicate entry: An entity attribute with the provided values already exists.')

            for field_id, value in fields.items():
                lf = Query.LinkedAttributeField.filter(session, attribute_id, field_id)

                if lf is None:
                    raise Exception('Field {} not linked to attribute {}'.format(field_id, attribute_id))

                field = EntityAttributeField(attribute.id, lf.id, value)
                session.add(field)

    def sync_entity(self, entity_id):

        with session_scope() as session:
            entity = Query.Entity.get(session, entity_id)

            if entity is not None:
                entity_json = entity.json()
                entity_json['attributes'] = self.sync_entity_attrs(session, entity_id)

                return entity_json

    def sync_entity_attrs(self, session, entity_id):

        attrs = {}

        for e_attr in [e.json() for e in Query.EntityAttribute.filter(session, entity_id)]:

            attr = Query.Attribute.get(session, e_attr['attribute_id'])
            attr_json = attr.json()

            e_attr['fields'] = []

            fields = [f.json() for f in Query.EntityAttributeField.filter(session, e_attr['id'])]

            for field in fields:
                lf = Query.LinkedAttributeField.get(session, field['linked_field_id']).json()
                af = Query.AttributeField.get(session, lf['field_id']).json()
                field['xml_id'] = af['id']
                field['name'] = af['name']
                e_attr['fields'].append(field)

            if attrs.get(e_attr['attribute_id']) is None:

                attr_json['data'] = [e_attr]
                attrs[attr.id] = attr_json

            else:
                attrs[e_attr['attribute_id']]['data'].append(e_attr)

        return attrs

    def sync_entities(self):

        with session_scope() as session:
            entity_json = {e.id: e.json() for e in Query.Entity.all(session)}

            for entity_id in entity_json.keys():
                entity_json[entity_id]['attributes'] = self.sync_entity_attrs(session, entity_id)

            return entity_json

    def upload_xml(self):

        for dirpath, dnames, fnames in os.walk(FileConfig.DATA_DIR):
            for f in fnames:
                filename = os.path.join(dirpath, f)
                if f.endswith(".xml"):
                    entities = run_entity_extraction(filename)
                    if entities is not None:
                        log.info('Entity extraction successful, starting import')
                        import_entities(entities)
                os.remove(filename)

    def sync_synic(self):

        return {
            'url': SynicAPI.synthesys_url(exclude_auth=True),
            'user': AppConfig.SYNTHESYS_USER,
            'api': SynicAPI.check_connection(),
            'knowledge_graphs': SynicAPI.get_knowledge_graphs(),
            'has_ee_pipeline': SynicAPI.has_ee_pipeline()
        }

    def ingest_entities(self, kg_name):

        if get_elapsed_minutes(self.last_ingestion_ts, max_on_null_value=True) < 10:
            raise Exception('Last ingestion time was recent. Please wait at least 10 minutes before each ingestion.')

        entity_json = self.sync_entities()
        export_entity_xml(entity_json)
        task_id = SynicAPI.ingest(kg_name)
        self.last_ingestion_ts = datetime.now()
        return {'taskId': task_id}
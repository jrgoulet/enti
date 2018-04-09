from enti.tasks import initialize_defaults, initialize_attributes, import_entities
from enti.query import Query
from enti.database import session_scope
from enti.settings import FileConfig
from enti.utils.parser import run_entity_extraction
import os
from enti.extensions import log
from enti.models import EntityAttribute, EntityAttributeField
from pprint import pprint


class Controller:

    def __init__(self):
        pass

    def initialize(self):
        initialize_defaults()
        initialize_attributes()

    def sync_attributes(self):

        with session_scope() as session:

            attr_json = {a.id:a.json() for a in Query.Attribute.all(session)}

            for attr_id in attr_json.keys():

                linked_fields = {
                    lf.field_id:Query.AttributeField.get(session, lf.field_id).json()
                    for lf in Query.LinkedAttributeField.filter(session, attr_id)
                }

                attr_json[attr_id]['fields'] = linked_fields

            return attr_json


    def update_attribute(self, field_id, value):

        with session_scope() as session:

            field = Query.EntityAttributeField.get(session, field_id)

            if field is None:

                raise Exception('Entity Attribute Field not found')

            else:

                old_val = field.value
                log.info('Updating field {} value from {} to {}'.format(field_id, old_val, value))

                field.value = value

    def remove_attribute(self, attribute_id):

        with session_scope() as session:

            attribute = Query.EntityAttribute.get(session, attribute_id)
            fields = Query.EntityAttributeField.filter(session, attribute_id)

            for field in fields:
                session.delete(field)

            session.delete(attribute)

    def add_attribute(self, entity_id, attribute_id, fields):

        with session_scope() as session:
            attribute = EntityAttribute(entity_id, attribute_id)
            session.add(attribute)
            session.commit()

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

            entity_json = {e.id:e.json() for e in Query.Entity.all(session)}

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





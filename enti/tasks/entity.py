# -*- coding: utf-8 -*-

from enti.database import session_scope
from enti.extensions import celery, log
from enti.definitions import AttributeTypes, EntityTypes, ArityTypes, AttributeFields
from enti.utils.parser import load_yml
from enti.settings import FileConfig
from enti.models import Attribute, LinkedAttributeField, Entity, EntityType, EntityAttribute
from enti.query import Query

@celery.task()
def import_entities(entities_json):

    log.info('Importing entities')

    with session_scope() as session:

        for e in entities_json:
            entity_id = e['id']
            entity = Query.Entity.get(session, entity_id)

            if entity is None:
                if Query.EntityType.get(session, e['type']) is None:
                    session.add(EntityType(id=e['type'],
                                           name=e['type'].replace('_',' ').title()))
                entity = Entity(id=e['id'],
                                name=e['name'],
                                type=e['type'],
                                canonical=e['canonical'])

                log.info('Adding {} entity {} (id: {})'.format(entity.type, entity.name, entity.id))
                session.add(entity)

            else:
                entity.name = e['name']
                entity.type = e['type']
                entity.canonical = e['canonical']
                log.info('Updating {} entity {} (id: {})'.format(entity.type, entity.name, entity.id))


            for a in e['attributes']:
                attr_id = a.pop('id', None)
                attribute = Query.Attribute.get(session, attr_id)

                if attribute is None:
                    log.error('Entity attribute {} for entity {} is undefined, skipping.'.format(attr_id, entity_id))

                    if a.get('sid') is not None:
                        attr_type = 'entity'
                    else:
                        attr_type = 'string'

                    session.add(Attribute(id=attr_id,
                                          name=attr_id.title(),
                                          required=False,
                                          arity=ArityTypes.FEW.id,
                                          ko_name=None,
                                          description='attribute added via XML import',
                                          type=attr_type))
                    session.commit()

                    for field_id in a.keys():
                        session.add(LinkedAttributeField(attr_id, field_id))

                for field_id, value in a.items():
                    field = Query.AttributeField.get(session, field_id)

                    if field is None:
                        log.error('Undefined field {} for attribute {} for entity {}, skipping.'.format(field_id, attr_id, entity_id))

                    else:
                        linked_field = Query.LinkedAttributeField.filter(session, attr_id, field_id)

                        if linked_field is None:
                            log.error(
                                'Field {} not allowed for attribute {} for entity {}, skipping.'.format(field_id,
                                                                                                      attr_id,
                                                                                                      entity_id))
                        else:
                            # TODO: Arity enforcement
                            existing_attrs = Query.EntityAttribute.filter(session, entity_id, linked_field.id)

                            duplicate = False

                            # Can't make unique key constraints with UTF8MB4 fields, so we check here for duplicates
                            for existing_attr in existing_attrs:
                                if existing_attr.value == value:
                                    duplicate = True

                            if not duplicate:
                                entity_attr = EntityAttribute(entity_id, attr_id, linked_field.id, value)
                                session.add(entity_attr)

                            else:
                                log.info('Skipped duplicate attribute {}:{} for entity {}'.format(attr_id, value, entity_id))
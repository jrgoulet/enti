# -*- coding: utf-8 -*-

from enti.database import session_scope
from enti.extensions import celery, log
from enti.definitions import AttributeTypes, EntityTypes, ArityTypes, AttributeFields
from enti.utils.parser import load_yml
from enti.settings import FileConfig
from enti.models import Attribute, LinkedAttributeField, Entity, EntityType, EntityAttribute, EntityAttributeField
from enti.query import Query


@celery.task()
def clean_empty_entity_attrs():

    with session_scope() as session:
        entity_attrs = Query.EntityAttribute.all(session)
        for entity_attr in entity_attrs:
            fields = Query.EntityAttributeField.filter(session, entity_attribute_id=entity_attr.id)

            if len(fields) == 0:
                log.info('Removing empty Entity Attribute: {} ({})'.format(entity_attr.id, entity_attr.entity_id))
                session.delete(entity_attr)

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
                                           name=e['type'].replace('_', ' ').title()))
                    session.commit()

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

                existing_attrs = Query.EntityAttribute.filter(session, entity_id, attr_id)
                duplicate = False

                for existing_attr in existing_attrs:
                    if duplicate:
                        break

                    matches = 0
                    num_fields = len(a)

                    for field_id, value in a.items():
                        field = Query.AttributeField.get(session, field_id)

                        if field is not None:
                            linked_field = Query.LinkedAttributeField.filter(session, attr_id, field_id)
                            existing_attr_field = Query.EntityAttributeField.filter(session, existing_attr.id,
                                                                                    linked_field.id)

                            if existing_attr_field is not None and existing_attr_field.value == value:
                                matches += 1

                    if matches == num_fields:
                        log.info('Duplicate field identified, skipping.')
                        duplicate = True

                if not duplicate:
                    entity_attr = EntityAttribute(entity_id, attr_id)
                    session.add(entity_attr)

                    for field_id, value in a.items():
                        field = Query.AttributeField.get(session, field_id)

                        if field is None:
                            log.error(
                                'Undefined field {} for attribute {} for entity {}, skipping.'.format(field_id, attr_id,
                                                                                                      entity_id))
                        else:
                            linked_field = Query.LinkedAttributeField.filter(session, attr_id, field_id)

                            if linked_field is None:
                                log.error(
                                    'Field {} not allowed for attribute {} for entity {}, skipping.'.format(field_id,
                                                                                                            attr_id,
                                                                                                            entity_id))
                            else:
                                # TODO: Arity enforcement
                                ea_field = EntityAttributeField(entity_attr.id, linked_field.id, value)
                                session.add(ea_field)

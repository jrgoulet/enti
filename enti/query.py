from enti.models import AttributeType, ArityType, Attribute, EntityType, Entity, AttributeField, LinkedAttributeField, \
    EntityAttribute, EntityAttributeField


class Query:
    class Attribute:
        @staticmethod
        def get(session, id):
            return session.query(Attribute).get(id)

        @staticmethod
        def all(session):
            return session.query(Attribute).all()

    class AttributeType:
        @staticmethod
        def get(session, id):
            return session.query(AttributeType).get(id)

        @staticmethod
        def all(session):
            return session.query(AttributeType).all()

    class ArityType:
        @staticmethod
        def get(session, id):
            return session.query(ArityType).get(id)

        @staticmethod
        def all(session):
            return session.query(ArityType).all()

    class EntityType:
        @staticmethod
        def get(session, id):
            return session.query(EntityType).get(id)

        @staticmethod
        def all(session):
            return session.query(EntityType).all()

    class Entity:
        @staticmethod
        def get(session, id):
            return session.query(Entity).get(id)

        @staticmethod
        def all(session):
            return session.query(Entity).all()

    class EntityAttribute:
        @staticmethod
        def get(session, id):
            return session.query(EntityAttribute).get(id)

        @staticmethod
        def all(session):
            return session.query(EntityAttribute).all()

        @staticmethod
        def filter(session, entity_id, attribute_id=None):
            if attribute_id is None:
                return session.query(EntityAttribute).filter(EntityAttribute.entity_id == entity_id).all()

            return session.query(EntityAttribute).filter(
                EntityAttribute.entity_id == entity_id,
                EntityAttribute.attribute_id == attribute_id
            ).all()

    class AttributeField:
        @staticmethod
        def get(session, id):
            return session.query(AttributeField).get(id)

        @staticmethod
        def all(session):
            return session.query(AttributeField).all()

    class LinkedAttributeField:
        @staticmethod
        def get(session, id):
            return session.query(LinkedAttributeField).get(id)

        @staticmethod
        def all(session):
            return session.query(LinkedAttributeField).all()

        @staticmethod
        def filter(session, attribute_id, field_id=None):
            if field_id is not None:
                return session.query(LinkedAttributeField).filter(
                    LinkedAttributeField.attribute_id == attribute_id,
                    LinkedAttributeField.field_id == field_id
                ).first()
            return session.query(LinkedAttributeField).filter(LinkedAttributeField.attribute_id == attribute_id).all()

    class EntityAttributeField:
        @staticmethod
        def get(session, id):
            return session.query(EntityAttributeField).get(id)

        @staticmethod
        def all(session):
            return session.query(EntityAttributeField).all()

        @staticmethod
        def filter(session, entity_attribute_id, linked_field_id=None):
                if linked_field_id is None:
                    return session.query(EntityAttributeField).filter(
                        EntityAttributeField.entity_attribute_id == entity_attribute_id).all()
                return session.query(EntityAttributeField).filter(
                    EntityAttributeField.entity_attribute_id == entity_attribute_id,
                    EntityAttributeField.linked_field_id == linked_field_id
                ).first()


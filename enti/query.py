from enti.models import AttributeType, ArityType, Attribute, EntityType, Entity, AttributeField, LinkedAttributeField, EntityAttribute


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
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Unicode, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from .base import Base
from enti.utils import generate_uuid

class Entity(Base):
    """External Entity model"""

    __tablename__ = 'Entity'
    id = Column(String(128), primary_key=True)
    name = Column(String(256), nullable=False)
    type = Column(String(128), ForeignKey('EntityType.id'), nullable=False)
    canonical = Column(Boolean, nullable=False)

    attribute = relationship("EntityAttribute",cascade="all, delete-orphan")

    def __init__(self, name, type, canonical, id=None):
        self.uuid = id if id is not None else generate_uuid()
        self.id = id
        self.name = name
        self.type = type
        self.canonical = canonical

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'canonical': self.canonical
        }

class EntityAttribute(Base):
    """Attributes that are tied to Entities"""

    __tablename__ = 'EntityAttribute'
    id = Column(String(128), primary_key=True)
    entity_id = Column(String(128), ForeignKey('Entity.id'), nullable=False)
    attribute_id = Column(String(128), ForeignKey('Attribute.id'), nullable=False)

    field = relationship("EntityAttributeField",cascade="all, delete-orphan")

    def __init__(self, entity_id, attribute_id):
        self.id = generate_uuid()
        self.entity_id = entity_id
        self.attribute_id = attribute_id


    def json(self):
        return {
            'id': self.id,
            'entity_id': self.entity_id,
            'attribute_id': self.attribute_id,
        }


class EntityAttributeField(Base):
    """Fields that are tied to EntityAttributes"""

    __tablename__ = 'EntityAttributeField'
    id = Column(String(128), primary_key=True)
    entity_attribute_id = Column(String(128), ForeignKey('EntityAttribute.id'), nullable=False)
    linked_field_id = Column(String(128), ForeignKey('LinkedAttributeField.id'), nullable=False)
    value = Column(Unicode(2048, collation='utf8mb4_unicode_ci'), nullable=True)

    def __init__(self, entity_attribute_id, linked_field_id, value):
        self.id = generate_uuid()
        self.entity_attribute_id = entity_attribute_id
        self.linked_field_id = linked_field_id
        self.value = value

    def json(self):
        return {
            'id': self.id,
            'entity_attribute_id': self.entity_attribute_id,
            'linked_field_id': self.linked_field_id,
            'value': self.value
        }

class EntityType(Base):
    """Enumeration of recognized entity types"""

    PERSON = 0
    GPE = 1
    LOCATION = 2
    FIN_INST = 3
    PHONE = 4
    ORGANIZATION = 5
    GOV_ORG = 6
    MILITARY = 7
    BUSINESS = 8
    ACADEMIC = 9

    __tablename__ = 'EntityType'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }


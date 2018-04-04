# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from .base import Base
from enti.utils import generate_uuid

class Entity(Base):
    """External Entity model"""

    __tablename__ = 'Entity'
    id = Column(String(128), primary_key=True)
    name = Column(String(256), nullable=False)
    type = Column(String(128), ForeignKey('EntityType.id'), nullable=False)
    canonical = Column(Boolean, nullable=False)

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


# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from .base import Base
from enti.utils import generate_uuid

class Attribute(Base):
    """Attribute Model"""

    __tablename__ = 'Attribute'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)
    ko_name = Column(String(128), nullable=True)
    description = Column(String(256), nullable=True)
    required = Column(Boolean, default=False, nullable=False)
    arity_id = Column(String(128), ForeignKey('ArityType.id'), nullable=False)
    type_id = Column(String(128), ForeignKey('AttributeType.id'), nullable=False)

    def __init__(self, name, required, arity, ko_name, description, type, id=None):
        self.id = id if id is not None else generate_uuid()
        self.name = name
        self.required = required
        self.arity_id = arity
        self.ko_name = ko_name
        self.description = description
        self.type_id = type

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'required': self.required,
            'arity': self.arity_id,
            'ko_name': self.ko_name,
            'description': self.description,
            'type': self.type_id
        }

class AttributeField(Base):
    """Field that holds a contextual value for a given attribute"""

    __tablename__ = 'AttributeField'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)

    def __init__(self, id, name):
        self.id = id,
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class LinkedAttributeField(Base):

    __tablename__ = 'LinkedAttributeField'
    id = Column(String(128), primary_key=True)
    attribute_id = Column(String(128), ForeignKey('Attribute.id'), nullable=False)
    field_id = Column(String(128), ForeignKey('AttributeField.id'), nullable=False)

    def __init__(self, attribute_id, field_id):
        self.id = '{}_{}'.format(attribute_id, field_id)
        self.attribute_id = attribute_id
        self.field_id = field_id

    def json(self):
        return {
            'id': self.id,
            'attribute_id': self.attribute_id,
            'field_id': self.field_id
        }



class AttributeType(Base):
    """Enumeration of recognized attribute types"""

    BOOLEAN = 0
    INTEGER = 1
    ENTITY = 2
    NAMED_REFERENCE = 3
    DATE = 4
    STRING = 5

    __tablename__ = 'AttributeType'
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

class ArityType(Base):
    """Enumeration of recognized arity types"""

    ONE = 1
    FEW = 2
    MANY = 3

    __tablename__ = 'ArityType'
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
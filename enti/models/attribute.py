# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from .base import Base
from enti.utils import generate_uuid

class Attribute(Base):
    """Attribute Model"""

    __tablename__ = 'Attribute'
    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)
    display_name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    required = Column(Boolean, default=False, nullable=False)
    arity = Column(Integer, ForeignKey('ArityType.id'), nullable=False)
    type = Column(Integer, ForeignKey('AttributeType.id'), nullable=False)

    def __init__(self, name, required, arity, display_name, description, type, id=None):
        self.id = id if id is not None else generate_uuid()
        self.name = name
        self.required = required
        self.arity = arity
        self.display_name = display_name
        self.description = description
        self.type = type

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'required': self.required,
            'arity': self.arity,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.type
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
    id = Column(Integer, primary_key=True)
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
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
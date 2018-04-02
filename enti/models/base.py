# -*- coding: utf-8 -*-

import json
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.ext.mutable import Mutable

Base = declarative_base()

class JSON(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
    """
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        """
        Converts dictionary value into a string, overriding the default SQLAlchemy method
        :param value: dict
        :param dialect: SQL dialect
        :return:
        """
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """
        Converts JSON string into a dictionary when retrieved from database
        :param value: string
        :param dialect: SQL dialect
        :return:
        """
        if value is not None:
            value = json.loads(value)
        return value


class MutableDict(Mutable, dict):

    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class BaseMixin():
    """
    Base mixin for use with all models

    Contains common methods and attributes
    """
    created_ts = Column(DateTime(), nullable=False)
    updated_ts = Column(DateTime(), nullable=False)
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def set_attrs(model):
        """
        Sets model attributes from keyword arguments

        :param model: model
        :return:
        """
        model.created_ts = datetime.now()
        model.updated_ts = datetime.now()

    def __repr__(self):
        return '{}'.format(self.__class__)

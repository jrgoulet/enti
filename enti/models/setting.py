# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean
from .base import Base
from enti.utils.encryption import AESCipher

class Setting(Base):
    """General application settings"""

    __tablename__ = 'Setting'
    id = Column(String(128), primary_key=True)
    name = Column(String(256), nullable=False)
    value = Column(String(1024), nullable=True)
    encrypted = Column(Boolean, default=False, nullable=False)
    sensitive = Column(Boolean, default=False, nullable=False)

    def __init__(self, id, name, value, encrypted=False, sensitive=False):
        self.id = id
        self.name = name

        if encrypted:
            self.value = AESCipher().encrypt_utf8(value)
        else:
            self.value = value

        self.encrypted = encrypted
        self.sensitive = sensitive

    def json(self, display_sensitive=False, decrypt_value=True):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.safe_value(display_sensitive, decrypt_value),
            'encrypted': self.encrypted,
            'sensitive': self.sensitive
        }

    def safe_value(self, display_sensitive=False, decrypt_value=True):
        if self.sensitive and not display_sensitive:
            return '****'
        elif self.encrypted and decrypt_value:
            return AESCipher().decrypt_utf8(self.value)
        else:
            return self.value


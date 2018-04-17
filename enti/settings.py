# -*- coding: utf-8 -*-

import os


class SynthesysConfig:
    ENTITIES_SRC = os.environ.get('ENTITIES_SRC', 'enti')
    SYNTHESYS_HOST = os.environ.get('SYNTHESYS_HOST', '0.0.0.0')
    SYNTHESYS_PORT = os.environ.get('SYNTHESYS_PORT', '8999')
    SYNTHESYS_SSL = os.environ.get('SYNTHESYS_SSL', 'false')
    SYNTHESYS_USER = os.environ.get('SYNTHESYS_USER', 'admin')
    SYNTHESYS_PASS = os.environ.get('SYNTHESYS_PASS', 'pass')
    INSTALL_DIR = os.environ.get('INSTALL_DIR', '/')

class UIConfig:
    FLASK_RELOAD = True
    RELOAD = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

class FileConfig:
    SRC_ROOT = os.path.join(os.curdir, 'enti')

    EXPORT_FILENAME = 'export.xml'

    SCHEMA_DIR = os.path.abspath(os.path.join(SRC_ROOT,'schema'))
    DATA_DIR = os.path.abspath(os.path.join(SRC_ROOT,'data'))
    EXPORT_DIR = os.path.abspath(os.path.join(SRC_ROOT,'export'))
    ATTR_SCHEMA_FILE = os.path.join(SCHEMA_DIR,'attributes.yml')
    EXPORT_FILE = os.path.join(EXPORT_DIR,EXPORT_FILENAME)

    RELATIVE_SRC_ROOT = 'enti'
    RELATIVE_EXPORT_DIR = os.path.join(RELATIVE_SRC_ROOT, 'export')
    RELATIVE_EXPORT_FILE = os.path.join(RELATIVE_EXPORT_DIR, EXPORT_FILENAME)

class DBConfig:
    DB_TYPE = os.environ.get('DATABASE_TYPE', 'mysql')
    DB_NAME = os.environ.get('DATABASE_NAME', 'enti')
    DB_HOST = os.environ.get('DATABASE_HOST', 'mysql')
    DB_PORT = os.environ.get('DATABASE_PORT', '3306')
    DB_USER = os.environ.get('DATABASE_USER', 'root')
    DB_PASS = os.environ.get('DATABASE_PASS', 'root')

    DB_URI = SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        DB_TYPE, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
    )

class CeleryConfig:
    BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379')
    BACKEND_URL = os.environ.get('CELERY_BACKEND_URL', 'redis://redis:6379')

class AppConfig(CeleryConfig, DBConfig, UIConfig, FileConfig, SynthesysConfig):
    MODE = os.environ.get('DEPLOYMENT_MODE', 'development')
    SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = os.environ.get('SERVER_PORT', 5100)
    ROLE = os.environ.get('ROLE', 'worker')

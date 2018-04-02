# -*- coding: utf-8 -*-

import os


class SynthesysConfig:
    SYNTHESYS_HOST = os.environ.get('SYNTHESYS_HOST', '0.0.0.0')
    SYNTHESYS_PORT = os.environ.get('SYNTHESYS_PORT', '8999')
    SYNTHESYS_USER = os.environ.get('SYNTHESYS_USER', 'admin')
    SYNTHESYS_PASS = os.environ.get('SYNTHESYS_PASS', 'pass')

class UIConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

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

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
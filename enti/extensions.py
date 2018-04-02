import warnings
from enti.utils.logger import Logger
from celery import Celery
from enti.settings import CeleryConfig
from sqlalchemy.ext.declarative import declarative_base
from flask.exthook import ExtDeprecationWarning
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_bcrypt import Bcrypt

warnings.simplefilter('ignore', ExtDeprecationWarning)

# SocketIO Server
socketio = SocketIO()

# BCrypt Encryption Utility
bcrypt = Bcrypt()

# Cross-Origin Resource Sharing
cors = CORS()

# SQLAlchemy Declarative Base
Base = declarative_base()

# Application Log Utility
log = Logger()

# Asynchronous Task Management
celery = Celery(
    'enti.tasks',
    broker=CeleryConfig.BROKER_URL,
    backend=CeleryConfig.BACKEND_URL
)



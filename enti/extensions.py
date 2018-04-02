from enti.utils.logger import Logger
from celery import Celery
from enti.settings import CeleryConfig
from sqlalchemy.ext.declarative import declarative_base

celery = Celery(
    'enti.tasks',
    broker=CeleryConfig.BROKER_URL,
    backend=CeleryConfig.BACKEND_URL
)

Base = declarative_base()

log = Logger()

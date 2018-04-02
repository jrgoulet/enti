from enti.database import init_db
from enti.extensions import celery as _celery, log

celery = _celery



@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Configures periodic tasks

    Runs on startup for celery containers
    """
    init_db()

@celery.task()
def say_hello():
    log.info('Hello')
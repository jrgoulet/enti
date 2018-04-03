from enti.database import init_db
from enti.extensions import celery, log


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Configures periodic tasks

    Runs on startup for celery containers
    """
    sender.add_periodic_task(60, say_hello, name='Health Check')
    init_db()

@celery.task()
def say_hello():
    log.info('Hello')
from enti.database import init_db
from enti.extensions import celery, log
from .initialization import initialize_defaults, initialize_attributes
from .entity import import_entities, clean_empty_entity_attrs

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Configures periodic tasks

    Runs on startup for celery containers
    """
    sender.add_periodic_task(60, clean_empty_entity_attrs, name='Clean Entity Attributes')
    init_db()

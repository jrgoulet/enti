# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from time import sleep

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker, scoped_session

from enti.extensions import celery, log
from enti.models import MODELS
from enti.settings import DBConfig
from enti.definitions import AttributeTypes, EntityTypes, ArityTypes, AttributeFields, ApplicationDefaults
from enti.utils.parser import load_yml
from enti.settings import FileConfig
from enti.models import Attribute, LinkedAttributeField
from enti.query import Query

engine = create_engine(DBConfig.DB_URI,
                       convert_unicode=True,
                       pool_recycle=3600,
                       pool_size=100)

Session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=True))


class DatabaseTask(Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        Session.remove()


def init_db():
    """Initializes SQLAlchemy database tables
    Models must be imported before schema creation

    Schema is not currently configured to migrate / update automatically
    Database volume must be re-initialized manually upon schema updates
    If database is not volume-mounted, just delete the container

    """
    def initialize_settings():
        """Initializes application settings"""
        log.debug('Initializing application settings')
        with session_scope() as session:
            for setting in ApplicationDefaults.list():
                try:
                    existing_setting = Query.Setting.get(session, setting.id)

                    if existing_setting is None:
                        log.debug('Initializing application default: {} -> {}'.format(setting.id, setting.safe_value()))
                        session.add(setting)
                    else:
                        log.debug(
                            'Application default exists: {} -> {}'.format(setting.id, setting.safe_value()))
                except Exception as e:
                    log.error('Failed to initialize setting: {} due to: {}'.format(setting.id, str(e)))
        log.debug('Application setting initialization complete')

    def initialize_entity_schema():
        """Initializes entity schema"""
        log.debug('Initializing entity schema defaults')
        with session_scope() as session:
            for defaults in AttributeTypes.list(), EntityTypes.list(), ArityTypes.list(), AttributeFields.list():
                for default in defaults:
                    def_type = type(default)
                    try:
                        def_existing = session.query(def_type).get(default.id)

                        if def_existing is None:
                            log.debug('Initializing default {}: {}'.format(def_type.__name__, default.name))
                            session.add(default)
                        # else:
                        #     log.debug('Entry exists for {}: {}'.format(def_type.__name__, default.name))
                    except Exception as e:
                        log.error(
                            'Failed to add default {}: {} due to: {}'.format(def_type.__name__, default.name, str(e)))
                        session.rollback()
        log.debug('Entity initialization complete')

    def initialize_attributes():
        """Initializes default attributes"""
        log.debug('Initializing attribute defaults')
        with session_scope() as session:
            attr_templates = load_yml(FileConfig.ATTR_SCHEMA_FILE)

            for attr_id, attr_template in attr_templates.items():
                try:
                    attribute = Attribute(id=attr_id,
                                          name=attr_template['name'],
                                          required=attr_template.get('required', False),
                                          arity=attr_template['arity'],
                                          ko_name=attr_template['ko_name'],
                                          description=attr_template['description'],
                                          type=attr_template['type'])
                    attribute_existing = Query.Attribute.get(session, attr_id)

                    if attribute_existing is None:
                        log.debug('Initializing attribute: {}'.format(attribute.name))
                        session.add(attribute)

                    # else:
                    #     log.debug('Attribute exists, skipping: {}'.format(attribute.name))

                    for field_id in attr_template['fields']:
                        attr_field = Query.AttributeField.get(session, field_id)

                        if attr_field is not None:
                            linked_attr_field = LinkedAttributeField(attribute.id, attr_field.id)
                            linked_attr_field_existing = Query.LinkedAttributeField.get(session, linked_attr_field.id)

                            if linked_attr_field_existing is None:
                                log.debug('Creating linked attribute field {} for attribute {}'.format(attr_field.name,
                                                                                                       attribute.name))
                                session.add(linked_attr_field)
                        else:
                            log.error('Attribute field {} is not defined in field definitions. Please add field to '
                                      'enumeration located in definitions.py. Skipping for now.'.format(field_id))
                except Exception as e:
                    log.error('Failed to initialize attribute: {} due to: {}'.format(attr_id, str(e)))
        log.debug('Attribute initialization complete')

    initialized = False
    while not initialized:
        try:
            add_engine_pidguard(engine)
            set_tx_isolation(engine)
            celery.Task = DatabaseTask

            for model in MODELS:
                if not engine.dialect.has_table(engine, model.__tablename__):
                    model.__table__.create(engine)

            #initialize_settings()
            initialize_entity_schema()
            initialize_attributes()

            initialized = True

            log.info('Database initialized')

        except Exception as e:
            log.exception(e)
            log.info('Waiting for database to initialize')
            sleep(5)


def set_tx_isolation(engine):
    # try:
    #     engine.execute('SET GLOBAL transaction_isolation=\'READ-COMMITTED\';')
    # except:
    #     engine.execute('SET GLOBAL tx_isolation=\'READ-COMMITTED\';')
    # log.info('Set MYSQL global transation isolation level to READ-COMMITTED')
    pass


def add_engine_pidguard(engine):
    """Adds multiprocessing guards.

    Forces a connection to be reconnected if it is detected as having been shared to a sub-process.
    """

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info.get('pid') != pid:
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
            )


@contextmanager
def session_scope():
    """
    Provides a transactional scope around a series of database operations
    """
    session = Session()

    try:
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()

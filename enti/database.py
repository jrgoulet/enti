# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from time import sleep

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session

from enti.extensions import celery, log
from enti.models import MODELS
from enti.settings import DBConfig

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

    initialized = False
    while not initialized:
        try:
            add_engine_pidguard(engine)
            set_tx_isolation(engine)
            celery.Task = DatabaseTask

            for model in MODELS:
                if not engine.dialect.has_table(engine, model.__tablename__):
                    model.__table__.create(engine)

            initialized = True
            log.info('Database initialized')

        except Exception as e:
            # log.exception(e)
            log.info('Waiting for database to initialize', whistle=False)
            sleep(5)

    log.info('Database connection established', whistle=False)


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

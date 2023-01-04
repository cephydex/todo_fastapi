import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.conf import settings
from fastapi_utils.guid_type import setup_guids_postgresql
from logging import Logger
from config.logconf import LOGGER_NAME


engine = sqlalchemy.create_engine(
        settings.db_url, echo=True,
    )
setup_guids_postgresql(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
log = Logger(LOGGER_NAME)

def get_db():
    """ Get database session

    Yields:
        SessionLocal: db
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_init():
    """ Create DB table using model objects
    """
    # create table for models that inherit from Base model
    Base.metadata.create_all(bind=engine)
    log.info("DB initialized & model table(s) created")


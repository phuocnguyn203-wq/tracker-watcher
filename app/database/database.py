from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app import config

class Base(DeclarativeBase):
    pass

engine = create_engine(config.settings.database_url)
DeclarativeBase.metadata.create_all(engine)

LocalSession = sessionmaker(engine)

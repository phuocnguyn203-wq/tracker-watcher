from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app import config

class Base(DeclarativeBase):
    pass

engine = create_engine(
    config.settings.database_url,
    connect_args={'check_same_thread': False}
)


LocalSession = sessionmaker(engine)

#create tables and avoid circular import
def init_db():
    from app.models import models
    Base.metadata.create_all(engine)
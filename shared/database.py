import os

import sqlalchemy
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from shared.config import Config

# Define the database URI

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

# Create the SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# Create a base class for declarative models
# Base = sqlalchemy.orm.declarative_base()
Base = declarative_base()


# For initial database setup
def init_db():
    from backend.models.menu import Menu
    from backend.models.item import Item
    from backend.models.role import Role
    from backend.models.user import User
    Base.metadata.create_all(bind=engine)

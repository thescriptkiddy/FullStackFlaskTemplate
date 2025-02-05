import os

import sqlalchemy
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from shared.config import Config

# TODO Refactor to reflect config.py settings
# Define the database URI
# DATABASE_URI = 'sqlite:///app.db'  # Adjust this as needed for your database
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

# Create the SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# Create a base class for declarative models
Base = sqlalchemy.orm.declarative_base()


# For initial database setup
def init_db():
    Base.metadata.create_all(bind=engine)

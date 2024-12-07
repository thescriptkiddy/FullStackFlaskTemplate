import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URI
# DATABASE_URI = 'sqlite:///app.db'  # Adjust this as needed for your database
DATABASE_URI = os.environ.get('DB_URI')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a scoped session
db_session = scoped_session(Session)

# Create a base class for declarative models
Base = sqlalchemy.orm.declarative_base()

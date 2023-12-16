import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# create a PostgreSQL engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create a session local class for session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a declarative base meta class
Base = declarative_base()

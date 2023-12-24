import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")

# create a PostgreSQL engine
DATABASE_URL = os.environ.get("DATABASE_URL")


engine = create_engine(DATABASE_URL)

# create a session local class for session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a declarative base meta class
Base = declarative_base()


def get_db():  # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

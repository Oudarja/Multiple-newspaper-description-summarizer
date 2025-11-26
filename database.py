# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

# Use pymysql as MySQL driver
pymysql.install_as_MySQLdb()

DATABASE_URL = "mysql+pymysql://root:destinationred002@localhost:3306/newsbd2"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


# Create database session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for ORM models
Base = declarative_base()
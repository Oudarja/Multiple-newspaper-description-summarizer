# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
from dotenv import load_dotenv
import os
load_dotenv() 
DB_PASS = os.getenv("password")
# Use pymysql as MySQL driver
pymysql.install_as_MySQLdb()

DATABASE_URL = f"mysql+pymysql://root:{DB_PASS}@localhost:3306/newsbd2"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


# Create database session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for ORM models
Base = declarative_base()
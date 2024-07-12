from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_PORT = os.getenv('MYSQL_PORT')
DATABASE = os.getenv('MYSQL_DATABASE')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
SCHEMA_NAME = os.getenv('MYSQL_DATABASE')
DATABASE_NAME = os.getenv('MYSQL_DATABASE')

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_database():
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))

def create_schema():
    global engine
    engine = create_engine(f"{DB_URL}{DATABASE_NAME}?charset-utf8")
    SessionLocal.configure(bind=engine)
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))

def drop_tables():
    Base.metadata.drop_all(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
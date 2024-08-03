from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

from ..core import settings

load_dotenv()

DATABASE_URL = settings.database_url
db_name = DATABASE_URL.split('/')[-1].split('?')[0]

base_db_url = DATABASE_URL.rsplit('/', 1)[0]

engine = create_engine(base_db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_database():
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

def create_schema():
    global engine
    engine = create_engine(DATABASE_URL)
    SessionLocal.configure(bind=engine)
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {db_name}"))

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
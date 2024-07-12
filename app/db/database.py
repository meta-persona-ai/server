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

# DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}?charset-utf8"

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
SCHEMA_NAME = "persona"
DATABASE_NAME = "persona"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_database():
    # 데이터베이스를 생성합니다.
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))

def create_schema():
    # 데이터베이스가 존재하면 해당 스키마를 사용하도록 연결 문자열을 업데이트합니다.
    global engine
    engine = create_engine(f"{DB_URL}{DATABASE_NAME}?charset-utf8")
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))

def create_tables():
    # 테이블을 생성합니다.
    Base.metadata.create_all(bind=engine)


# engine = create_engine(DB_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def create_schema():
#     with engine.connect() as connection:
#         connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DATABASE}"))

# def create_tables():
#     Base.metadata.create_all(bind=engine)

# create_schema()
# create_tables()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
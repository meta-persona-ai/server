from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest
import os

from app.db.database import Base, get_db
from app.db.initial_data import DatabaseInitializer

from app.main import app

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
base_db_url = DATABASE_URL.split('?')[0]
db_name = base_db_url.rsplit('/', 1)[-1]
base_db_url = base_db_url.rsplit('/', 1)[0]

TEST_DATABASE_URL = f"{base_db_url}/test_db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"charset": "utf8mb4"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    test_engine = create_engine(
        base_db_url,
        connect_args={"charset": "utf8mb4"}
    )

    with test_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS test_db CHARACTER SET utf8mb4"))

    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"charset": "utf8mb4"}
    )

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    initializer = DatabaseInitializer(test_engine, data_file='app/resources/init_data.yaml')
    initializer.init_db()

    yield test_engine
    # Base.metadata.drop_all(bind=test_engine)
    # with test_engine.connect() as connection:
    #     connection.execute(text("DROP DATABASE IF EXISTS test_db"))

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

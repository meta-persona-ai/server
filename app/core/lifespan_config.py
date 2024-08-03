from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core import settings
from app.db import database
from app.db.initial_data import DatabaseInitializer
from app.utils.webhook import server_start_message, server_stop_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    server_start_message()

    database.create_database()
    database.create_schema()
    database.drop_tables()
    database.create_tables()

    initializer = DatabaseInitializer(database.engine, data_file='app/resources/init_data.yaml')
    initializer.init_db()

    yield

    server_stop_message()
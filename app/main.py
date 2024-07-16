from fastapi import FastAPI
from contextlib import asynccontextmanager

from core import swagger_config
from database import create_database, create_schema, drop_tables, create_tables
from domain.auth import auth_router
from domain.user import user_router
from domain.etc import etc_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    create_schema()
    # drop_tables()
    create_tables()
    yield

app = FastAPI(
    title=swagger_config.title,
    description=swagger_config.description,
    version=swagger_config.version,
    openapi_tags=swagger_config.tags_metadata,
    lifespan=lifespan
    )


# Including API routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(etc_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

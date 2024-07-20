from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.swagger_config import SwaggerConfig
from app.db.database import create_database, create_schema, drop_tables, create_tables
from app.db.initial_data import init_db
from app.api.v1 import auth_router, user_router, character_router, chat_router, etc_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    create_schema()
    drop_tables()
    create_tables()

    init_db()

    yield

swagger_config = SwaggerConfig()
config = swagger_config.get_config()

app = FastAPI(
    title=config["title"],
    description=config["description"],
    version=config["version"],
    license_info=config["license_info"],
    openapi_tags=config["tags_metadata"],
    lifespan=lifespan
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# Including API routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(character_router.router)
app.include_router(chat_router.router)
app.include_router(etc_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

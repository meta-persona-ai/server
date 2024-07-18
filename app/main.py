from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core import swagger_config
from app.database import create_database, create_schema, drop_tables, create_tables
from app.domain.auth import auth_router
from app.domain.user import user_router
from app.domain.character import character_router
from app.domain.chat import chat_router
from app.domain.etc import etc_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    create_schema()
    drop_tables()
    create_tables()
    yield

app = FastAPI(
    title=swagger_config.title,
    description=swagger_config.description,
    version=swagger_config.version,
    openapi_tags=swagger_config.tags_metadata,
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

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os


from swagger_info import description, tags_metadata
from routers import user_router
from database import create_database, create_schema, drop_tables, create_tables
from domain.auth import auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    create_schema()
    drop_tables()
    create_tables()
    yield

app = FastAPI(
    title="Persona AI",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    lifespan=lifespan
    )


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


# Including API routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
# app.include_router(user_router.router, prefix="/api/crud", tags=["user"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

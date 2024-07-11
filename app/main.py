from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

from app.api import auth_router


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


# Including API routers
app.include_router(auth_router.router, prefix="/api/auth")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

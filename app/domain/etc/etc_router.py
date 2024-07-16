from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os


router = APIRouter(
    prefix="",
    tags=["etc"]
)

@router.get("/", response_class=HTMLResponse)
async def serve_homepage():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
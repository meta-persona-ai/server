from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse
import os

from ...utils.s3_util import upload_to_s3


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

@router.post("/upload")
async def upload_file(file: UploadFile):
    url = await upload_to_s3(file)
    return {"url": url}

@router.get("/chatting", response_class=HTMLResponse)
async def serve_chatting():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "chatting.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@router.get("/image", response_class=HTMLResponse)
async def serve_image():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    file_path = os.path.join(project_root, "app", "templates", "image_view.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
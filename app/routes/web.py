from fastapi import Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from app.controllers.ZipController import ZipController
import os

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

def register_routes(app, templates):
    zip_controller = ZipController(templates)

    @app.get("/", response_class=HTMLResponse, tags=["Web"])
    async def index(request: Request):
        return zip_controller.index(request)

    @app.post("/upload", tags=["API"])
    async def upload(file: UploadFile = File(...), rename_map: str = Form(...)):
        return await zip_controller.upload(file, rename_map)


    @app.get("/download/{filename}", tags=["API"])
    async def download(filename: str):
        return zip_controller.download(filename)
    
    @app.delete("/cleanup", tags=["API"])
    async def cleanup():
        return zip_controller.cleanup()


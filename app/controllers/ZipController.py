import os
import uuid
import json
from fastapi import UploadFile, Form
from fastapi.responses import FileResponse
from app.services.ZipService import ZipService

class ZipController:
    def __init__(self, templates):
        self.templates = templates
        self.zip_service = ZipService()

    def index(self, request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def upload(self, file: UploadFile, rename_map: str = Form(...)):
        uid = str(uuid.uuid4())
        zip_path = os.path.join("uploads", f"{uid}.zip")

        if not file.filename.endswith(".zip"):
            return { "error": "Only .zip files are allowed." }

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        try:
            rename_dict = json.loads(rename_map)
        except Exception:
            return { "error": "Rename map must be valid JSON. Example: {\"round\": \"A01\"}" }

        renamed_zip, renamed_files, validation_errors = self.zip_service.process_zip(zip_path, uid, rename_dict)

        if validation_errors:
            return { "error": "\n".join(validation_errors) }

        if not renamed_files:
            return { "error": "No files matched the rename map." }

        return {
            "download_url": f"/download/{os.path.basename(renamed_zip)}",
            "renamed_files": renamed_files
        }

    def download(self, filename: str):
        file_path = os.path.join("results", filename)
        return FileResponse(file_path, media_type="application/zip", filename=filename)
    
    def cleanup(self):
        removed = self.zip_service.cleanup()
        return { "message": "Cleanup complete.", "removed": removed }

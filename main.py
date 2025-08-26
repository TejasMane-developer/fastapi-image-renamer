import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.web import register_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read from .env
APP_NAME = os.getenv("APP_NAME", "Image Renamer API")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Upload a zip of images and get renamed images with preview.")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
register_routes(app, templates)

if __name__ == "__main__":
    import uvicorn
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)

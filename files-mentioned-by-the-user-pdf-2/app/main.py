import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, chat
from app.db.database import Base, engine
from app import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("support_chat")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support Chat Bot API", version="1.0.0")
app.include_router(auth.router)
app.include_router(chat.router)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    if response.status_code >= 400:
        logger.warning("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(static_dir / "index.html")

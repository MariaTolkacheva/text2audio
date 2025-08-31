import logging
import os

from database import Base, engine
from fastapi import FastAPI
from routers import jobs

logger = logging.getLogger("fastapi")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/storage")

# Create tables on startup (simple first version)
Base.metadata.create_all(bind=engine)

api = FastAPI(title="Text → Audiobook API (v1)")
api.include_router(jobs.router)


@api.post("/ping")
def upload_text() -> str:
    logger.error("Just health check on errors really")
    return "pong"

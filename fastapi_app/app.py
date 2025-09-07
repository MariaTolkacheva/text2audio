import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from pydantic import BaseModel

from fastapi_app.database import Base, engine
from fastapi_app.routers import jobs

logger = logging.getLogger("fastapi")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/storage")


class HealthCheckResponse(BaseModel):
    status: str
    message: str = "pong"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application startup and shutdown events."""
    logger.info(
        "Starting up and creating database tables %s if they do not exist.", app.title
    )
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down.")


api = FastAPI(title="Text → Audiobook API (v1)", lifespan=lifespan)
api.include_router(jobs.router)


# Define the health check endpoint
@api.get(
    "/ping",
    summary="Health Check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponse,
)
def ping() -> HealthCheckResponse:
    """
    A simple health check endpoint to verify the API is running.
    """
    logger.info("Health check ping received.")
    return HealthCheckResponse(status="healthy")

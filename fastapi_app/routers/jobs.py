import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from fastapi_app.cache import get_status, set_status
from fastapi_app.crud import create_job, get_job
from fastapi_app.database import get_db
from fastapi_app.schemas import JobCreate, JobOut
from fastapi_app.tasks import generate_audio

logger = logging.getLogger(__name__)

STORAGE_DIR = os.getenv("STORAGE_DIR", "/storage")
router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/upload-text")
def upload_text(data: dict):
    return {"received your data": data}


@router.post("/jobs", response_model=JobOut)
def create_conversion(payload: JobCreate, db: Session = Depends(get_db)):
    job = create_job(db, user=payload.user or "anonymous", text=payload.text)
    set_status(job.id, "PENDING")
    logging.info("Created a job with id=%d", job.id)
    generate_audio.delay(job.id)
    return JobOut(job_id=job.id, status="PENDING")


@router.get("/jobs/{job_id}", response_model=JobOut)
def job_status(job_id: int, db: Session = Depends(get_db)):
    # Fast path: Redis
    cached = get_status(job_id)
    if cached:
        return JobOut(job_id=job_id, status=cached)
    # Fallback: DB
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return JobOut(job_id=job.id, status=job.status)


@router.get("/jobs/{job_id}/download")
def download(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.status != "DONE" or not job.audio_file:
        raise HTTPException(409, "Not ready")
    path = job.audio_file
    if not os.path.exists(path):
        raise HTTPException(410, "File missing")
    filename = f"job-{job_id}.wav"
    return FileResponse(path, media_type="audio/wav", filename=filename)

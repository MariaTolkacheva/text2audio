from sqlalchemy.orm import Session

from .models import Job


def create_job(db: Session, user: str, text: str) -> Job:
    job = Job(user=user, text=text, status="PENDING")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job_status(
    db: Session, job_id: int, status: str, audio_file: str | None = None
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    job.status = status
    if audio_file:
        job.audio_file = audio_file
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, job_id: int) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()

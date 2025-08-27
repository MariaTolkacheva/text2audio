import os

from cache import set_status
from celery import Celery
from crud import get_job, update_job_status
from database import SessionLocal
from sqlalchemy.orm import Session
from utils_audio import synth_to_file

BROKER = os.getenv("CELERY_BROKER_URL")
BACKEND = os.getenv("CELERY_RESULT_BACKEND")
STORAGE_DIR = os.getenv("STORAGE_DIR", "/storage")

app = Celery("tts_tasks", broker=BROKER, backend=BACKEND)


@app.task(name="tts.generate_audio")
def generate_audio(job_id: int):
    db: Session = SessionLocal()
    try:
        # mark running
        update_job_status(db, job_id, "RUNNING")
        set_status(job_id, "RUNNING")

        job = get_job(db, job_id)
        if not job:
            set_status(job_id, "FAILED")
            return {"ok": False, "error": "job not found"}

        # do the fake TTS
        out_path = os.path.join(STORAGE_DIR, f"{job_id}.wav")
        synth_to_file(job.text, out_path)

        # mark done
        update_job_status(db, job_id, "DONE", audio_file=out_path)
        set_status(job_id, "DONE")
        return {"ok": True, "path": out_path}
    except Exception as e:
        update_job_status(db, job_id, "FAILED")
        set_status(job_id, "FAILED")
        return {"ok": False, "error": str(e)}
    finally:
        db.close()

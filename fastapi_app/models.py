from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from fastapi_app.database import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, default="anonymous", index=True)
    text = Column(Text)
    status = Column(
        String, default="PENDING", index=True
    )  # PENDING/RUNNING/DONE/FAILED
    audio_file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

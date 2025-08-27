from pydantic import BaseModel


class JobCreate(BaseModel):
    user: str | None = "anonymous"
    text: str

class JobOut(BaseModel):
    job_id: int
    status: str
    class Config:
        from_attributes = True

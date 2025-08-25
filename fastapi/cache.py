import os

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def set_status(job_id: int, status: str, ttl: int = 3600):
    r.set(f"job:{job_id}:status", status, ex=ttl)


def get_status(job_id: int) -> str | None:
    return r.get(f"job:{job_id}:status")

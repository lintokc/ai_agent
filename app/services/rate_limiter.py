import redis
from fastapi import Request, HTTPException
from app.config import config

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

RATE_LIMIT = 5  # 5 requests per minute
TIME_WINDOW = 60  # seconds

def rate_limiter(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    request_count = redis_client.get(key)

    if request_count and int(request_count) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    redis_client.incr(key)
    redis_client.expire(key, TIME_WINDOW)

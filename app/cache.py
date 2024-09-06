import aioredis
from fastapi import Depends
from redis.asyncio import Redis
from .config import settings

redis = None

async def get_redis() -> Redis:
    global redis
    if not redis:
        redis = await aioredis.from_url(f"redis://{settings.redis_hostname}:{settings.redis_port}/{settings.redis_db}")
    return redis

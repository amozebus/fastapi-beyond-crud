"""JTI blocklist initialization"""
import redis.asyncio as aioredis

from config import settings

redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

jti_blocklist = aioredis.from_url(redis_url)
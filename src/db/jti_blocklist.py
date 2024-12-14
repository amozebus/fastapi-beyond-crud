"""JTI blocklist initialization"""

import redis.asyncio as aioredis

from config import settings

REDIS_URL = (
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

jti_blocklist = aioredis.from_url(REDIS_URL)

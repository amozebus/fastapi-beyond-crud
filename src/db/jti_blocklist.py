"""JTI blocklist initialization"""

import redis.asyncio as aioredis

from config import settings

jti_blocklist = aioredis.from_url(settings.JTI_BLOCKLIST_URL)

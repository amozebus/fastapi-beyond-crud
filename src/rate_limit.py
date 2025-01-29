"""Requests rate limiter"""

import time

from functools import wraps

from typing import Callable, Any

from fastapi import Request, Response, HTTPException


def rate_limit(max_calls: int, period: int):
    """Limiting requests rate by max calls in time period (in seconds)"""

    def decorator(func: Callable[[Request], Any]) -> Callable[[Request], Any]:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs) -> Response:
            if not request.client:
                raise ValueError("Request has no client information")
            ip_address: str = request.client.host

            # update the timestamps
            now = time.time()
            if ip_address not in usage:
                usage[ip_address] = []
            timestamps = usage[ip_address]
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) < max_calls:
                timestamps.append(now)
                return await func(request, *args, **kwargs)

            wait = period - (now - timestamps[0])
            raise HTTPException(
                status_code=429,
                headers={"Retry-After": f"{int(wait)}"},
                detail="Rate limit exceeded. Try again later",
            )

        return wrapper

    return decorator

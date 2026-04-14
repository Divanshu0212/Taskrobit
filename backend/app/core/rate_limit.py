import math

from fastapi import HTTPException, status

from app.config import get_settings
from app.core.cache import get_redis_client


settings = get_settings()


def enforce_login_rate_limit(identifier: str) -> None:
    try:
        client = get_redis_client()
        key = f"login_limit:{identifier}"
        current = client.incr(key)
        if current == 1:
            client.expire(key, settings.rate_limit_window_seconds)

        if current > settings.rate_limit_login_attempts:
            ttl = client.ttl(key)
            retry_after = max(1, math.ceil(ttl)) if ttl and ttl > 0 else settings.rate_limit_window_seconds
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many login attempts. Retry after {retry_after} seconds.",
            )
    except Exception:
        # Keep auth available even if Redis is temporarily unavailable.
        return

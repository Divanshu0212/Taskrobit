import json
from typing import Any

import redis

from app.config import get_settings


settings = get_settings()


def get_redis_client() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)


def cache_set_json(key: str, value: dict[str, Any], ttl_seconds: int | None = None) -> None:
    client = get_redis_client()
    client.setex(key, ttl_seconds or settings.cache_ttl_seconds, json.dumps(value))


def cache_get_json(key: str) -> dict[str, Any] | None:
    client = get_redis_client()
    raw = client.get(key)
    if not raw:
        return None
    return json.loads(raw)


def cache_delete(key: str) -> None:
    client = get_redis_client()
    client.delete(key)

import asyncio
import random
from typing import Callable, Any, Awaitable

async def backoff_retry(coro_fn: Callable[[], Awaitable[Any]], *, retries: int = 3, base_ms: int = 200, jitter_ms: int = 100):
    """
    Retries an async callable up to `retries` times with exponential backoff + jitter.
    coro_fn must be an async callable with zero args.
    """
    exc = None
    for attempt in range(retries):
        try:
            return await coro_fn()
        except Exception as e:
            exc = e
            if attempt == retries - 1:
                break
            sleep_ms = (2 ** attempt) * base_ms + random.randint(0, jitter_ms)
            await asyncio.sleep(sleep_ms / 1000.0)
    raise exc

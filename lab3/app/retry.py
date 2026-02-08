import asyncio
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    retries: int = 3,
    base_delay_s: float = 0.5,
    retry_if: Optional[Callable[[Exception], bool]] = None,
) -> T:
    """
    Retry an async operation with exponential backoff.
    If retry_if is provided, only retry when retry_if(e) returns True.
    """
    last_exception = None
    for attempt in range(retries + 1):
        try:
            return await fn()
        except Exception as e:
            last_exception = e
            if retry_if is not None and not retry_if(e):
                raise
            if attempt < retries:
                delay = base_delay_s * (2**attempt)
                await asyncio.sleep(delay)
            else:
                raise last_exception
    raise last_exception  # unreachable but satisfies type checker

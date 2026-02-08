"""Unit tests for ToDo 2: Retries and timeouts (retry_async)."""

import asyncio
import time
import pytest

from app.retry import retry_async


@pytest.mark.asyncio
async def test_retry_succeeds_on_first_try():
    """Should return result immediately when fn succeeds."""
    call_count = 0

    async def succeeds() -> str:
        nonlocal call_count
        call_count += 1
        return "ok"

    result = await retry_async(succeeds)
    assert result == "ok"
    assert call_count == 1


@pytest.mark.asyncio
async def test_retry_succeeds_after_failures():
    """Should succeed after N failures and return result."""
    call_count = 0

    async def fails_twice_then_succeeds() -> int:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return 42

    result = await retry_async(fails_twice_then_succeeds, retries=3)
    assert result == 42
    assert call_count == 3


@pytest.mark.asyncio
async def test_retry_raises_after_all_retries_exhausted():
    """Should raise the last exception when all retries fail."""
    call_count = 0

    async def always_fails() -> None:
        nonlocal call_count
        call_count += 1
        raise RuntimeError("always fails")

    with pytest.raises(RuntimeError, match="always fails"):
        await retry_async(always_fails, retries=3, base_delay_s=0.01)

    assert call_count == 4  # 1 initial + 3 retries


@pytest.mark.asyncio
async def test_retry_zero_retries_raises_immediately():
    """With retries=0, should only try once then raise."""
    call_count = 0

    async def fails() -> None:
        nonlocal call_count
        call_count += 1
        raise OSError("nope")

    with pytest.raises(OSError, match="nope"):
        await retry_async(fails, retries=0)

    assert call_count == 1


@pytest.mark.asyncio
async def test_retry_exponential_backoff_timing():
    """Delays should follow exponential backoff (base * 2^attempt)."""
    call_times = []
    attempt = 0

    async def fails_until_third() -> str:
        nonlocal attempt
        call_times.append(time.monotonic())
        attempt += 1
        if attempt < 3:
            raise ValueError("retry")
        return "done"

    result = await retry_async(fails_until_third, retries=5, base_delay_s=0.05)
    assert result == "done"

    # Check delays: ~0.05, ~0.1 between calls
    if len(call_times) >= 3:
        d1 = call_times[1] - call_times[0]
        d2 = call_times[2] - call_times[1]
        assert d1 >= 0.04  # ~0.05
        assert d2 >= 0.08  # ~0.1 (2x base)

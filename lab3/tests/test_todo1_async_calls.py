"""Unit tests for ToDo 1: Concurrent async calls (run_many, run_many_with_limit)."""

import asyncio
import time
import pytest

from app.runner import run_many, run_many_with_limit


@pytest.fixture
def async_sleep_fn():
    """Simulated async function that sleeps and returns transformed input."""

    async def fn(s: str) -> str:
        await asyncio.sleep(0.05)
        return s.upper()

    return fn


@pytest.fixture
def async_identity_fn():
    """Simple async identity for fast tests."""

    async def fn(s: str) -> str:
        return s

    return fn


@pytest.mark.asyncio
async def test_run_many_returns_results_in_order(async_sleep_fn):
    """Results must match input order."""
    prompts = ["a", "b", "c"]
    results = await run_many(async_sleep_fn, prompts)
    assert results == ["A", "B", "C"]


@pytest.mark.asyncio
async def test_run_many_runs_concurrently(async_sleep_fn):
    """Concurrent execution should be faster than sequential."""
    prompts = [str(i) for i in range(10)]
    start = time.monotonic()
    results = await run_many(async_sleep_fn, prompts)
    elapsed = time.monotonic() - start
    assert results == [str(i).upper() for i in range(10)]
    # Sequential would take ~0.5s; concurrent should be ~0.05s
    assert elapsed < 0.2


@pytest.mark.asyncio
async def test_run_many_empty_list(async_identity_fn):
    """Empty prompts returns empty list."""
    results = await run_many(async_identity_fn, [])
    assert results == []


@pytest.mark.asyncio
async def test_run_many_single_prompt(async_sleep_fn):
    """Single prompt works correctly."""
    results = await run_many(async_sleep_fn, ["hello"])
    assert results == ["HELLO"]


@pytest.mark.asyncio
async def test_run_many_with_limit_returns_results_in_order(async_sleep_fn):
    """run_many_with_limit must preserve output order."""
    prompts = ["x", "y", "z"]
    results = await run_many_with_limit(async_sleep_fn, prompts, limit=2)
    assert results == ["X", "Y", "Z"]


@pytest.mark.asyncio
async def test_run_many_with_limit_limits_concurrency():
    """Verify at most 'limit' tasks run at once."""
    in_flight = 0
    max_in_flight = 0

    async def track_concurrency(s: str) -> str:
        nonlocal in_flight, max_in_flight
        in_flight += 1
        max_in_flight = max(max_in_flight, in_flight)
        await asyncio.sleep(0.05)
        in_flight -= 1
        return s

    prompts = [str(i) for i in range(10)]
    results = await run_many_with_limit(track_concurrency, prompts, limit=2)
    assert max_in_flight <= 2
    assert results == prompts


@pytest.mark.asyncio
async def test_run_many_with_limit_empty_list(async_identity_fn):
    """Empty prompts with limit returns empty list."""
    results = await run_many_with_limit(async_identity_fn, [], limit=2)
    assert results == []


@pytest.mark.asyncio
async def test_run_many_with_limit_one_prompt(async_sleep_fn):
    """Single prompt with limit works correctly."""
    results = await run_many_with_limit(async_sleep_fn, ["test"], limit=1)
    assert results == ["TEST"]

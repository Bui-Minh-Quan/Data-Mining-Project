from __future__ import annotations

import time
from typing import Iterable, Iterator, List, Sequence

import requests

from .constants import BINANCE_BASE_URL, KLINES_ENDPOINT


def fetch_klines(
    symbol: str,
    interval: str,
    limit: int = 1000,
    start_time: int | None = None,
    end_time: int | None = None,
) -> List[List[int | float | str]]:
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": min(limit, 1000),
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time

    url = BINANCE_BASE_URL + KLINES_ENDPOINT
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected response format (not a list): {data}")
    return data


def paginate_klines(
    *,
    symbol: str,
    interval: str,
    start_ms: int,
    end_ms: int,
    limit: int = 1000,
    pause_seconds: float = 0.2,
) -> Iterator[Sequence[int | float | str]]:
    """
    Yield klines across the requested time window by issuing multiple API calls.
    """
    current = start_ms
    safe_limit = min(limit, 1000)

    while current < end_ms:
        batch = fetch_klines(
            symbol=symbol,
            interval=interval,
            limit=safe_limit,
            start_time=current,
            end_time=end_ms,
        )
        if not batch:
            break

        for row in batch:
            yield row

        last_close_time = batch[-1][6]
        next_start = last_close_time + 1
        if next_start <= current:
            break
        current = next_start

        if len(batch) < safe_limit:
            break

        time.sleep(pause_seconds)



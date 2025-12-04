from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence

from .constants import KLINES_HEADER


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_klines(rows: Iterable[Sequence], output_path: str) -> int:
    """
    Write klines rows to CSV. Returns number of rows written.
    """
    path = Path(output_path)
    ensure_parent(path)

    count = 0
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(KLINES_HEADER)
        for row in rows:
            writer.writerow(row[: len(KLINES_HEADER)])
            count += 1
    return count



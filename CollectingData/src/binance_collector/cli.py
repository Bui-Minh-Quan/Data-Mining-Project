from __future__ import annotations

import argparse
import time
from typing import Iterable, Sequence

from .api import fetch_klines, paginate_klines
from .csv_utils import write_klines
from .time_utils import date_to_millis
from .validators import parse_interval


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="binance-collector",
        description="Collect Binance BTC (or any symbol) data and export to CSV files.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    latest = subparsers.add_parser(
        "latest", help="Fetch up to 1000 klines in a single call."
    )
    _add_common_kline_args(latest, include_optional_range=True)
    latest.set_defaults(handler=_handle_latest)

    full_range = subparsers.add_parser(
        "range",
        help="Fetch klines across a long time range by paging multiple API calls.",
    )
    _add_common_kline_args(full_range, include_optional_range=False)
    full_range.add_argument(
        "--start",
        type=str,
        required=True,
        help="Start time (UTC) 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'",
    )
    full_range.add_argument(
        "--end",
        type=str,
        required=True,
        help="End time (UTC), same format as --start",
    )
    full_range.add_argument(
        "--pause",
        type=float,
        default=0.2,
        help="Pause (in seconds) between paged requests. Default: 0.2",
    )
    full_range.set_defaults(handler=_handle_range)

    return parser


def _add_common_kline_args(
    parser: argparse.ArgumentParser, *, include_optional_range: bool
) -> None:
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Trading symbol, e.g. BTCUSDT. Default: BTCUSDT",
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="1m",
        help="Kline interval, e.g. 1m, 5m, 15m, 1h, 4h, 1d. Default: 1m",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of klines to fetch (max 1000). Default: 500",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV path. When omitted, file name is auto-generated.",
    )
    if include_optional_range:
        parser.add_argument(
            "--start",
            type=str,
            default=None,
            help="Optional start time (UTC) 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'",
        )
        parser.add_argument(
            "--end",
            type=str,
            default=None,
            help="Optional end time (UTC), same format as --start",
        )


def _handle_latest(args: argparse.Namespace) -> None:
    interval = parse_interval(args.interval)
    start_ms = date_to_millis(args.start) if args.start else None
    end_ms = date_to_millis(args.end) if args.end else None
    limit = min(args.limit, 1000)
    output_path = args.output or _auto_filename(args.symbol, interval)

    print(
        f"Fetching up to {limit} klines for {args.symbol.upper()} "
        f"interval={interval}..."
    )

    rows = fetch_klines(
        symbol=args.symbol,
        interval=interval,
        limit=limit,
        start_time=start_ms,
        end_time=end_ms,
    )
    count = write_klines(rows, output_path)
    print(f"Wrote {count} klines to {output_path}")


def _handle_range(args: argparse.Namespace) -> None:
    interval = parse_interval(args.interval)
    start_ms = date_to_millis(args.start)
    end_ms = date_to_millis(args.end)
    if start_ms >= end_ms:
        raise ValueError("Start time must be earlier than end time.")
    limit = min(args.limit, 1000)
    output_path = args.output or _auto_filename(
        args.symbol, interval, suffix="_fullrange"
    )

    print(
        f"Fetching klines for {args.symbol.upper()} interval={interval} "
        f"from {args.start} to {args.end}..."
    )

    generator = paginate_klines(
        symbol=args.symbol,
        interval=interval,
        start_ms=start_ms,
        end_ms=end_ms,
        limit=limit,
        pause_seconds=args.pause,
    )
    count = write_klines(generator, output_path)
    print(f"Wrote {count} klines to {output_path}")


def _auto_filename(symbol: str, interval: str, suffix: str = "") -> str:
    timestamp = int(time.time())
    suffix_part = f"{suffix}_" if suffix else ""
    return f"{symbol.lower()}_{interval}_{suffix_part}{timestamp}.csv"


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    args.handler(args)



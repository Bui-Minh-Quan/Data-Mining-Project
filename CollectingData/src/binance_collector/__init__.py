"""
Binance data collection helpers.

Expose the main CLI via ``python -m binance_collector`` or by importing
``binance_collector.cli.main``.
"""

from .cli import main

__all__ = ["main"]



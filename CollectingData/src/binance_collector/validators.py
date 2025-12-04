from .constants import ALLOWED_INTERVALS


def parse_interval(interval: str) -> str:
    """
    Validate that interval matches Binance-supported values.
    """
    normalized = interval.strip()
    if normalized not in ALLOWED_INTERVALS:
        raise ValueError(
            f"Invalid interval '{interval}'. Expected one of: {sorted(ALLOWED_INTERVALS)}"
        )
    return normalized



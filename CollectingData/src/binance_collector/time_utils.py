from datetime import datetime, timezone


def date_to_millis(date_str: str) -> int:
    """
    Convert 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' (UTC) to epoch milliseconds.
    """
    text = date_str.strip()
    if len(text) == 10:
        text += " 00:00:00"
    dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)



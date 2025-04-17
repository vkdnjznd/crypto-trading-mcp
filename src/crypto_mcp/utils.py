import pytz

from datetime import datetime


def iso_to_timestamp(iso_date: str) -> int:
    """
    Convert ISO 8601 date string to Unix timestamp (milliseconds since epoch)

    Args:
        iso_date (str): ISO 8601 formatted date string (e.g. "2024-06-13T10:26:21+09:00")

    Returns:
        int: Unix timestamp in milliseconds
    """
    dt = datetime.fromisoformat(iso_date)
    return int(dt.timestamp() * 1000)


def timestamp_to_iso(timestamp: int, tz: str) -> str:
    """
    Convert Unix timestamp (milliseconds since epoch) to ISO 8601 date string
    """
    return datetime.fromtimestamp(timestamp / 1000, tz=pytz.timezone(tz)).isoformat()

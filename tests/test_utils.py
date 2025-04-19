from crypto_trading_mcp.utils import iso_to_timestamp, timestamp_to_iso


def test_iso_to_timestamp():
    test_date = "2024-06-13T10:26:21+09:00"
    expected_timestamp = 1718241981000  # milliseconds

    result = iso_to_timestamp(test_date)
    assert result == expected_timestamp, f"Expected {expected_timestamp}, got {result}"


def test_timestamp_to_iso():
    timestamp = 1718241981000  # milliseconds
    expected_iso = "2024-06-13T10:26:21+09:00"

    result = timestamp_to_iso(timestamp, "Asia/Seoul")
    assert result == expected_iso, f"Expected {expected_iso}, got {result}"

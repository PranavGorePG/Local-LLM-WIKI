from datetime import datetime, timezone

def get_current_timestamp() -> str:
    """Return a standard ISO 8601 timestamp string."""
    return datetime.now(timezone.utc).isoformat()

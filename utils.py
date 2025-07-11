from datetime import datetime, timezone
from pathlib import Path

def time_ago_from_epoch(epoch_str):
    # Convert the epoch string to float
    epoch = float(epoch_str)
    
    # Convert to datetime object
    last_updated = datetime.fromtimestamp(epoch, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    
    # Calculate the difference
    delta = now - last_updated
    seconds = delta.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours ago"
    elif seconds < 30 * 86400:
        return f"{int(seconds // 86400)} days ago"
    else:
        return last_updated.strftime("%Y-%m-%d")


def load_custom_css():
    """
    Load custom CSS styles for the Streamlit app.
    """
    css_file_path = Path(__file__).parent / "style.css"
    with open(css_file_path, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"

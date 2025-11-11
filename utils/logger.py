# utils/logger.py
"""Simple logger utility."""

import traceback
from datetime import datetime


def log_error(e: Exception):
    """Logs exceptions with timestamp."""
    print(f"[ERROR {datetime.now().strftime('%H:%M:%S')}] {e}")
    traceback.print_exc()

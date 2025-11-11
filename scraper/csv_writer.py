# scraper/csv_writer.py
"""Handles safe CSV writing for crypto data."""

import os


def atomic_write_csv(df, path):
    """Writes DataFrame to CSV atomically (safe overwrite)."""
    temp = path + ".tmp"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df.to_csv(temp, index=False)

    try:
        if os.path.exists(path):
            os.remove(path)
    except PermissionError:
        print("[!] CSV locked; please close it before the next write.")
        os.remove(temp)
        return

    os.rename(temp, path)
    print(f"[+] CSV updated successfully at {path}")

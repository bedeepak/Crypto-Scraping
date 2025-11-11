# main.py
"""Main entry point for Crypto Tracker project."""

import time
from config import CSV_FILE, REFRESH_SEC, TOP_N, URL, HEADLESS
from scraper.driver_setup import init_driver
from scraper.data_extractor import scrape_top_n
from scraper.csv_writer import atomic_write_csv
from utils.logger import log_error


def main():
    """Run the continuous crypto tracking loop."""
    driver = init_driver(headless=HEADLESS)
    try:
        while True:
            df = scrape_top_n(driver, URL, TOP_N)
            print(df)
            atomic_write_csv(df, CSV_FILE)
            time.sleep(REFRESH_SEC)
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        log_error(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

# scraper/data_extractor.py
"""Extracts cryptocurrency data from CoinMarketCap table."""

import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .header_mapper import map_table_headers


def scrape_top_n(driver, url: str, n: int):
    """Scrape top N cryptocurrencies with price, 24h change, and market cap."""
    driver.get(url)

    table_xpath = "//table[contains(@class,'cmc-table')]"
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, table_xpath + "/tbody/tr"))
    )

    header_map = map_table_headers(driver)
    rows = driver.find_elements(By.XPATH, table_xpath + "/tbody/tr")[:n]
    data = []

    for r in rows:
        try:
            # Extract coin name
            try:
                coin_link = r.find_element(By.XPATH, ".//a[contains(@href,'/currencies/')]")
                full_text = coin_link.text.strip()
                if " " in full_text:
                    name, symbol = full_text.rsplit(" ", 1)
                    coin_full = f"{name} ({symbol})"
                else:
                    coin_full = full_text
            except Exception:
                coin_full = r.find_element(By.XPATH, ".//p[contains(@class,'coin-item-symbol')]").text

            tds = r.find_elements(By.TAG_NAME, "td")
            price = tds[header_map.get("price", 0)].text.strip() if "price" in header_map else ""
            change_24h = tds[header_map.get("24h", 0)].text.strip() if "24h" in header_map else ""
            market_cap = tds[header_map.get("market_cap", 0)].text.strip() if "market_cap" in header_map else ""

            data.append([coin_full, price, change_24h, market_cap])
        except Exception:
            continue

    df = pd.DataFrame(data, columns=["Coin", "Price", "24h Change", "Market Cap"])
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df

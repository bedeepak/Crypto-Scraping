# scraper/header_mapper.py
"""Maps column headers of the CoinMarketCap table to their respective indices."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def map_table_headers(driver, timeout=15):
    """
    Reads <thead> of the main table and returns a dict mapping:
    'coin', 'price', '24h', 'market_cap' -> column index.
    """
    table_xpath = "//table[contains(@class,'cmc-table')]"
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, table_xpath + "//thead"))
    )
    ths = driver.find_elements(By.XPATH, table_xpath + "//thead//th")
    mapping = {}

    for idx, th in enumerate(ths):
        text = " ".join(th.text.strip().lower().split())
        if "name" in text or "asset" in text:
            mapping["coin"] = idx
        if "price" in text:
            mapping["price"] = idx
        if "24h" in text or "24 h" in text or "24h %" in text:
            mapping["24h"] = idx
        if "market cap" in text or "market" in text:
            mapping["market_cap"] = idx
    return mapping

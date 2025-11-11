# scraper/driver_setup.py
"""Handles setup of the Selenium WebDriver."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(headless: bool = True) -> webdriver.Chrome:
    """Initialize a Chrome WebDriver with standard options."""
    opts = Options()
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1400,1000")
    opts.add_argument("--log-level=3")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if headless:
        opts.add_argument("--headless=new")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

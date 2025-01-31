import time
from playwright.sync_api import sync_playwright
from config import HEADLESS, WAIT_TIME
from scraper.utils import logger


class BaseExtractor:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    def start_browser(self) -> None:
        """Start the browser"""
        logger.info("Starting the browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=HEADLESS)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logger.info("Browser started successfully.")

    def navigate(self, url: str) -> None:
        """Navigate to the specified page"""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        time.sleep(WAIT_TIME)
        logger.info(f"Navigation to {url} completed.")

    def close_browser(self) -> None:
        """Close the browser"""
        logger.info("Closing the browser...")
        self.browser.close()
        self.playwright.stop()
        logger.info("Browser closed.")

    def close_cookie_popup(self) -> None:
        """Close the cookie popup"""
        try:
            logger.info("Attempting to close the cookie popup...")
            self.page.locator("#onetrust-accept-btn-handler").click(timeout=6000)
            logger.info("Cookies closed.")
        except TimeoutError:
            logger.warning("Cookie popup not found.")

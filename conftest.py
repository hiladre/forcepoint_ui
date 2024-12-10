import os
import pytest
from playwright.sync_api import sync_playwright

# Create a folder for screenshots if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def playwright():
    """Start and yield the Playwright instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """Start and yield the browser instance (Chrome)."""
    browser = playwright.chromium.launch(headless=False)  # Set headless=True for headless mode
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Provide a new page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """Take a screenshot when a test fails."""
    if report.failed and hasattr(node.instance, "example_page"):
        page = node.instance.example_page.page  # Access the `page` from `example_page`
        test_name = node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        try:
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

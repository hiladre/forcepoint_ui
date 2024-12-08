import os

import pytest
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


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


@pytest.fixture(scope="class")
async def browser_context(request):
    """Set up and tear down resources at the class level using async API."""
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Attach resources to the test class instance
        request.cls.playwright = playwright
        request.cls.browser = browser
        request.cls.context = context
        request.cls.page = page

        yield  # Run the tests

        # Clean up resources after the tests
        await page.close()
        await context.close()
        await browser.close()


# Create a folder for screenshots if it doesn't exist
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    """Take a screenshot when a test fails."""
    # Check if the test failed and the test node has a 'page' attribute
    if report.failed and hasattr(node.instance, "page"):
        page = node.instance.page
        test_name = node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        try:
            # Capture the screenshot
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")


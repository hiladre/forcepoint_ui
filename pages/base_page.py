from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Get the title of the current page."""
        return self.page.title()

    def click_element(self, selector: str):
        """Click an element based on its selector."""
        self.page.click(selector)

    def fill_input(self, selector: str, value: str):
        """Fill an input field."""
        self.page.fill(selector, value)

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        return self.page.text_content(selector)

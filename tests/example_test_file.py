from pages.example_page import UltimatePage
import pytest


@pytest.mark.usefixtures("browser_context")
class TestExample:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.example_page = UltimatePage(page)

    def test_button_count(self):
        button_count = self.example_page.count_buttons_in_section()
        assert button_count == 12

    def test_facebook_links(self):
        self.example_page.verify_facebook_links()

    def test_form(self):
        self.example_page.fill_submit_form(name="hila", email="hila@gmail.com", message="blabla")




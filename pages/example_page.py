import re

from base_page import BasePage
from maps.button_map import ButtonMap
from maps.form_map import FormMap
from maps.social_media_map import SocialMedia


class UltimatePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.navigate_to("https://ultimateqa.com/complicated-page")

    def set_name(self, name):
        self.page.fill(FormMap.NAME, name)

    def set_email(self, email):
        self.page.fill(FormMap.EMAIL, email)

    def set_message(self, message):
        self.page.fill(FormMap.MESSAGE, message)

    def set_math(self):
        res = self.page.inner_text(FormMap.captcha_text)
        numbers = re.findall(r'\d+', res)
        if len(numbers) == 2:
            # Convert the extracted numbers to integers and calculate the sum
            num1, num2 = map(int, numbers)
            result = num1 + num2
            self.page.fill(FormMap.MATH, str(result))

    def submit(self):
        self.page.locator(FormMap.SUBMIT).first.click()

    def fill_submit_form(self, name, email, message):
        self.set_name(name)
        self.set_email(email)
        self.set_message(message)
        self.set_math()
        self.submit()
        self.page.wait_for_selector('text=Thanks for contacting us', timeout=5000)  # Adjust the selector as needed

        # Verify if the message is present
        if self.page.is_visible('text=Thanks for contacting us'):
            print("Success: 'Thanks for contacting us' message is displayed.")
        else:
            assert False

    def count_buttons_in_section(self):
        # Count buttons within the section
        section = self.page.locator(ButtonMap.SECTION_SELECTOR)
        buttons = section.locator(ButtonMap.BUTTON_SELECTOR)
        button_count = buttons.count()

        return button_count

    def verify_facebook_links(self):

        # Locate the section
        section = self.page.locator(SocialMedia.SECTION_SELECTOR)

        # Find all buttons within the section
        buttons = section.locator(SocialMedia.BUTTON_SELECTOR)

        # Loop through each button and verify the href
        facebook_url = "https://www.facebook.com/Ultimateqa1/"
        all_valid = True

        for button in buttons.all():
            href = button.get_attribute('href')
            if href != facebook_url:
                print(f"Invalid href found: {href}")
                all_valid = False

        # Final result
        if all_valid:
            print("All Facebook button hrefs are correct.")
        else:
            assert False

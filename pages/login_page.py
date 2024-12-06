from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.locator("#login-button")
        self.invalid_login_error_msg = page.locator(".error-message-container")

    def set_username(self, username: str):
        self.username_input.fill(username)

    def set_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login_to_application(self, username: str, password: str):
        self.set_username(username)
        self.set_password(password)
        self.click_login()

    def get_error_msg_locator(self) -> Locator:
        return self.invalid_login_error_msg

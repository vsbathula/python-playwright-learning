from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utilities.read_config import AppConfiguration
from playwright.sync_api import expect
from utilities import constants


class TestLogin(BaseTest):

    configuration = AppConfiguration.get_users()

    def get_user_credentials(self, user_type):
        return {
            "username": self.configuration[user_type]["userName"],
            "password": self.configuration[user_type]["password"]
        }

    def test_user_login_with_valid_credentials(self):
        """
        Verify login with valid credentials.
        """
        self.login_page = LoginPage(self.page)
        print("Actual page title: {0}".format(self.login_page.get_page_title()))
        assert self.login_page.get_page_title() == constants.LOGIN_PAGE_TITLE
        creds = self.get_user_credentials("validUser")
        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

    def test_user_login_with_invalid_credentials(self):
        """
        Verify login with invalid credentials.
        """
        expected_error_msg = "Epic sadface: Username and password do not match any user in this service"

        self.login_page = LoginPage(self.page)
        creds = self.get_user_credentials("inValidUser")

        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_msg_locator()
        expect(actual_msg).to_have_text(expected_error_msg)

    def test_user_login_with_locked_out_credentials(self):
        """
        Verify login with locked out credentials.
        """
        expected_error_msg = "Epic sadface: Sorry, this user has been locked out."

        self.login_page = LoginPage(self.page)
        creds = self.get_user_credentials("lockedOutUser")

        # Perform login
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_msg_locator()
        expect(actual_msg).to_have_text(expected_error_msg)

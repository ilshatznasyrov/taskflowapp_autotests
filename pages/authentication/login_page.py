import re

from config import settings
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from pages.authentication.registration_page import RegistrationPage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.subtitle = page.locator(".subtitle")
        self.email_input = page.get_by_test_id("email-input")
        self.password_input = page.get_by_test_id("password-input")
        self.login_button = page.get_by_test_id("login-button")
        self.register_link = page.get_by_test_id("register-link")
        self.error_message = page.get_by_test_id("error-message")
        self.email_error_message = page.get_by_test_id("email-error")
        self.password_error_message = page.get_by_test_id("password-error")
        self.user_name = page.get_by_test_id("user-name")
        self.count = page.get_by_test_id("stat-total")


    def open_login_page(self):

        self.visit(f"{settings.app_url}/index.html")


    def check_visible(self):

        expect(self.subtitle).to_be_visible()
        expect(self.subtitle).to_have_text("Войдите в свой аккаунт")
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()


    def fill_login_form(self, email: str, password: str):

        self.email_input.fill(email)
        expect(self.email_input).to_have_value(email)

        self.password_input.fill(password)
        expect(self.password_input).to_have_value(password)


    def click_login_button(self):

        self.login_button.click()


    def click_register_link(self):

        self.register_link.click()


    def check_successful_login_with_role_user(self):

        expect(self.count).to_be_visible()
        expect(self.user_name).to_be_visible()


    def check_successful_login_with_role_admin(self):

        from pages.admin_panel.admin_panel_page import AdminPage

        admin_panel = AdminPage(self.page)
        admin_panel.check_visible()


    def check_visible_error_message(self, error_message_text: str):

        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(error_message_text)


    def check_email_validation_error(self):

        expect(self.email_error_message).to_be_visible()
        expect(self.email_input).to_have_class(re.compile(r".*\berror\b.*"))


    def check_password_validation_error(self):

        expect(self.password_error_message).to_be_visible()
        expect(self.password_input).to_have_class(re.compile(r".*\berror\b.*"))


    def check_visible_login_button(self):

        expect(self.login_button).to_be_visible()
        expect(self.login_button).to_have_text("Войти")


    def check_go_to_registration_page(self):

        registration_form = RegistrationPage(self.page)
        registration_form.check_visible()

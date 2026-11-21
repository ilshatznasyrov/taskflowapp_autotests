import allure

from config import settings
from pages.base_page import BasePage
from playwright.sync_api import Page, expect

from pages.dashboard.dashboard_page import DashboardPage


class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.subtitle = page.locator(".subtitle")
        self.username_input = page.get_by_test_id("name-input")
        self.name_error = page.get_by_test_id("name-error")
        self.email_input = page.get_by_test_id("email-input")
        self.email_error = page.get_by_test_id("email-error")
        self.password_input = page.get_by_test_id("password-input")
        self.password_error = page.get_by_test_id("password-error")
        self.confirm_password_input = page.get_by_test_id("confirm-password-input")
        self.confirm_password_error = page.get_by_test_id("confirm-password-error")
        self.register_button = page.get_by_test_id("register-button")
        self.login_link = page.get_by_test_id("login-link")
        self.success_message = page.get_by_test_id("success-message")
        self.error_message = page.get_by_test_id("error-message")
        self.dashboard_page = DashboardPage(page)


    def open_registration_page(self):

        self.visit(f"{settings.app_url}/register.html")


    def check_visible(self):

        expect(self.subtitle).to_be_visible()

        expect(self.username_input).to_be_visible()
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.confirm_password_input).to_be_visible()
        expect(self.register_button).to_be_visible()
        expect(self.login_link).to_be_visible()


    def fill_register_form(self, username: str, email: str, password: str):

        self.username_input.fill(username)
        expect(self.username_input).to_have_value(username)

        self.email_input.fill(email)
        expect(self.email_input).to_have_value(email)

        self.password_input.fill(password)
        expect(self.password_input).to_have_value(password)

        self.confirm_password_input.fill(password)
        expect(self.confirm_password_input).to_have_value(password)


    def click_register_button(self):

        self.register_button.click()


    @allure.step("Проверяем, что появилось сообщение об успешной регистрации")
    def check_visible_success_message(self):

        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_have_text("Успешно! Перенаправление...")


    def check_not_visible_success_message(self):

        expect(self.success_message).not_to_be_visible()


    def check_visible_error_message(self):

        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("Пользователь с таким email уже существует")


    def check_not_visible_error_message(self):

        expect(self.error_message).not_to_be_visible()


    def click_login_link(self):

        self.login_link.click()


    def check_subtitle(self):

        expect(self.subtitle).to_have_text("Создайте новый аккаунт")


    def check_name_error_message(self):

        expect(self.name_error).to_have_text("Имя должно содержать не менее 2 символов")


    def check_email_error_message(self):

        expect(self.email_error).to_have_text("Введите корректный email")


    def check_password_error_message(self):

        expect(self.password_error).to_have_text("Пароль должен быть не менее 6 символов")


    def check_confirm_password_error_message(self):

        expect(self.confirm_password_error).to_have_text("Пароли не совпадают")


    def check_open_dashboard_page(self):

        self.dashboard_page.check_counters_with_no_tasks()
        self.dashboard_page.check_toolbar()
        self.dashboard_page.check_tasks_list_with_no_tasks()


    def fill_register_form_with_incorrect_confirm_password(self, username: str, email: str, password: str):

        incorrect_confirm_password = f"{password}_Ilshat"

        self.username_input.fill(username)
        expect(self.username_input).to_have_value(username)

        self.email_input.fill(email)
        expect(self.email_input).to_have_value(email)

        self.password_input.fill(password)
        expect(self.password_input).to_have_value(password)

        self.confirm_password_input.fill(incorrect_confirm_password)
        expect(self.confirm_password_input).to_have_value(incorrect_confirm_password)


    @allure.step("Проверяем, что поле имени помечено как невалидное")
    def check_empty_name_field_validation(self):
        invalid_name_input = self.page.locator("[data-testid='name-input']:invalid")
        expect(invalid_name_input).to_be_visible()


    @allure.step("Проверяем, что поле пароля помечено как невалидное")
    def check_empty_password_field_validation(self):

        invalid_password_input = self.page.locator("[data-testid='password-input']:invalid")
        expect(invalid_password_input).to_be_visible()


    @allure.step("Проверяем, что поле email помечено как невалидное")
    def check_empty_email_field_validation(self):

        invalid_email_input = self.page.locator("[data-testid='email-input']:invalid")
        expect(invalid_email_input).to_be_visible()

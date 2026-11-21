import allure

from components.alert.alert_component import AlertComponent
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class EditPanelPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = page.get_by_test_id("modal-title")

        self.name_input = page.get_by_test_id("edit-name-input")
        self.name_label = page.locator("//label[@for='editName']")

        self.email_input = page.get_by_test_id("edit-email-input")
        self.email_label = page.locator("//label[@for='editEmail']")

        self.password_input = page.get_by_test_id("edit-password-input")
        self.password_label = page.locator("//label[@for='editPassword']")

        self.role_select = page.get_by_test_id("edit-role-select")
        self.role_label = page.locator("//label[@for='editRole']")

        self.save_button = page.get_by_test_id("save-edit-button")
        self.close_button = page.get_by_test_id("close-modal")

        self.alert = AlertComponent(page)


    @allure.step("Проверяем отображение панели редактирования")
    def check_visible(self):

        expect(self.title).to_be_visible()
        expect(self.title).to_have_text("Редактировать пользователя")

        expect(self.name_input).to_be_visible()
        expect(self.name_label).to_be_visible()
        expect(self.name_label).to_have_text("Имя")

        expect(self.email_input).to_be_visible()
        expect(self.email_label).to_be_visible()
        expect(self.email_label).to_have_text("Email")

        expect(self.password_input).to_be_visible()
        expect(self.password_label).to_be_visible()
        expect(self.password_label).to_have_text("Новый пароль (оставь пустым, чтобы не менять)")

        expect(self.role_select).to_be_visible()
        expect(self.role_label).to_be_visible()
        expect(self.role_label).to_have_text("Роль")

        expect(self.save_button).to_be_visible()
        expect(self.close_button).to_be_visible()


    @allure.step("Редактируем роль и сохраняем изменения")
    def change_role(self, role_value: str):

        self.role_select.select_option(value=role_value)
        self.save_button.click()
        self.alert.check_visible_alert_user_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Проверяем текущую роль")
    def check_current_role(self, role: str):

       expect(self.role_select).to_have_text(role)


    @allure.step("Редактируем имя и сохраняем изменения")
    def change_name(self, username: str):

        self.name_input.fill(username)
        self.save_button.click()
        self.alert.check_visible_alert_user_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Редактируем пароль и сохраняем изменения")
    def change_password(self, password: str):

        self.password_input.fill(password)
        self.save_button.click()
        self.alert.check_visible_alert_user_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Редактируем email и сохраняем изменения")
    def change_email(self, email: str):

        self.email_input.fill(email)
        self.save_button.click()
        self.alert.check_visible_alert_user_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Редактируем email и сохраняем изменения")
    def check_error_save_editing(self, email: str):

        self.email_input.fill(email)
        self.save_button.click()
        self.alert.check_visible_alert_error_save_editing()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Кликаем на крестик")
    def close(self):

        self.close_button.click()

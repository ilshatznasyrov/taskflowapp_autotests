import allure
from playwright.sync_api import Page, expect

from components.base_component import BaseComponent
from components.alert.alert_component import AlertComponent


class UserItemComponent(BaseComponent):

    def __init__(self, page: Page, name: str):
        super().__init__(page)

        self.alert = AlertComponent(page)

        self.user = (
            page.get_by_test_id("users-list")
            .locator(".user-item")
            .filter(has=page.locator(".user-name", has_text=name))
        )

        self.user_name = self.user.locator(".user-name")
        self.user_email = self.user.locator(".user-email")
        self.badge_admin = self.user.locator(".badge.badge-admin")
        self.badge_user = self.user.locator(".badge.badge-user")
        self.badge_active = self.user.locator(".badge.badge-active")
        self.badge_blocked = self.user.locator(".badge.badge-blocked")
        self.edit_btn = self.user.locator(".btn.btn-edit")
        self.block_btn = self.user.locator(".btn.btn-block")
        self.unblock_btn = self.user.locator(".btn.btn-unblock")
        self.delete_btn = self.user.locator(".btn.btn-delete")
        self.its_you_label = self.user.locator(".user-actions")


    @allure.step("Проверяем наличие пользователя")
    def check_visible(self):

        expect(self.user).to_be_visible()


    @allure.step("Проверяем отсутствие пользователя")
    def check_not_visible(self):

        expect(self.user).not_to_be_visible()


    @allure.step("Проверяем имя пользователя")
    def check_name(self, expected_name: str):

        expect(self.user_name).to_have_text(expected_name)


    @allure.step("Проверяем email пользователя")
    def check_email(self, expected_email: str):

        expect(self.user_email).to_have_text(expected_email)


    @allure.step("Проверяем роль 'Админ'")
    def check_admin_role(self):

        expect(self.badge_admin).to_have_text("Админ")


    @allure.step("Проверяем роль 'Пользователь'")
    def check_user_role(self):

        expect(self.badge_user).to_have_text("Пользователь")


    @allure.step("Проверяем статус 'Активен'")
    def check_status_active(self):

        expect(self.badge_active).to_have_text("Активен")


    @allure.step("Проверяем статус 'Заблокирован'")
    def check_status_blocked(self):

        expect(self.badge_blocked).to_have_text("Заблокирован")


    @allure.step("Проверяем статус 'Разблокирован'")
    def check_status_unblocked(self):

        expect(self.badge_active).to_have_text("Активен")


    @allure.step("Блокируем пользователя")
    def blocking_user(self):

        self.block_btn.click()
        self.alert.check_visible_confirm_of_block_user()
        self.alert.click_confirm_button_ok()
        self.alert.check_confirm_closed()
        self.alert.check_visible_alert_block_user()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Разблокируем пользователя")
    def unblocking_user(self):

        self.unblock_btn.click()
        self.alert.check_visible_confirm_of_unblock_user()
        self.alert.click_confirm_button_ok()
        self.alert.check_confirm_closed()
        self.alert.check_visible_alert_unblock_user()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    def delete_user(self):

        self.delete_btn.click()
        self.alert.check_visible_confirm_of_delete_user()
        self.alert.click_confirm_button_ok()
        self.alert.check_confirm_closed()
        self.alert.check_visible_alert_delete_user()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Проверяем наличие метки текущего пользователя")
    def check_its_you_label(self):

        expect(self.its_you_label).to_have_text("Это вы")


    def check_not_visible_delete_btn(self):

        expect(self.delete_btn).not_to_be_visible()


    @allure.step("Кликаем на кнопку 'Редактировать' у пользователя")
    def click_edit_btn(self):

        self.edit_btn.click()

        
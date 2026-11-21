import re

import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class NavbarComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.logo = page.locator("//div[@class=\"logo\"]")
        self.username_container = page.get_by_test_id("user-name")
        self.logout_button = page.get_by_test_id("logout-button")


    def check_visible_logo(self):

        expect(self.logo).to_be_visible()
        expect(self.logo).to_have_text("🐞 TaskFlow")


    def check_visible_username(self, username: str):

        expect(self.username_container).to_be_visible()
        expect(self.username_container).to_have_text(username)


    def check_visible_logout_button(self):

        expect(self.logout_button).to_be_visible()
        expect(self.logout_button).to_have_text("Выйти")


    @allure.step("Разлогиниваемся по клику на кнопку 'Выйти' и проверяем, что отображаются url и title страницы авторизации")
    def click_logout(self):

        self.logout_button.click()
        expect(self.page).to_have_url(re.compile(r".*index\.html$"))
        expect(self.page).to_have_title("TaskFlow — Вход в систему")


    def click_logo(self):

        self.logo.click()
        expect(self.page).to_have_title("TaskFlow — Мои задачи")

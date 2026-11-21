from typing import Pattern

import allure
from playwright.sync_api import Page, expect


class BaseComponent:
    
    def __init__(self, page: Page):
        self.page = page


    @allure.step("Проверяем, что отображается верный url")
    def check_current_url(self, expected_url: Pattern[str]):
        expect(self.page).to_have_url(expected_url)

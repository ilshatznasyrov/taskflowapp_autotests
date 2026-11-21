import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class StatCardComponent(BaseComponent):

    def __init__(self, page: Page, identifier: str, title: str):
        super().__init__(page)

        self.title_text = title

        self.counter_locator = page.get_by_test_id(f"stat-{identifier}")
        self.title_locator = page.locator(f"//div[@class=\"stat-label\" and text()=\"{title}\"]")

    def check_visible(self, counter: str):

        step_name = f"Проверяем, что карточка со статистикой '{self.title_text}' отображается и счетчик показывает '{counter}'"
        with allure.step(step_name):
            expect(self.counter_locator).to_be_visible()
            expect(self.counter_locator).to_have_text(counter)

            expect(self.title_locator).to_be_visible()

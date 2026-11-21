import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class ToolbarComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.search_input = page.get_by_test_id("search-input")
        self.status_filter = page.get_by_test_id("status-filter")
        self.priority_filter = page.get_by_test_id("priority-filter")
        self.add_task_button = page.get_by_test_id("add-task-button")


    def check_visible(self):

        expect(self.search_input).to_be_visible()
        expect(self.search_input).to_have_attribute(
            "placeholder", "🔍 Поиск задач..."
        )
        expect(self.status_filter).to_be_visible()
        expect(self.status_filter.locator("option:checked")).to_have_text("Все статусы")
        expect(self.priority_filter).to_be_visible()
        expect(self.priority_filter.locator("option:checked")).to_have_text("Все приоритеты")
        expect(self.add_task_button).to_be_visible()
        expect(self.add_task_button).to_have_text("+ Добавить задачу")


    def click_add_task_button(self):

        self.add_task_button.click()


    def check_search_input(self):

        expect(self.search_input).to_be_visible()


    def fill_text_in_search(self, text: str):

        self.search_input.fill(text)


    def clear_search(self):

        self.search_input.clear()
        expect(self.search_input).to_have_attribute(
            "placeholder", "🔍 Поиск задач..."
        )


    def check_filled_search_value_saved_in_input_field(self, search_query: str):

        expect(self.search_input).to_have_value(search_query)


    def select_filter_by_status(self, status: str):

        self.status_filter.select_option(status)


    def select_filter_by_priority(self, priority: str):

        self.priority_filter.select_option(priority)


    def check_filter_by_status_initial_state(self):

        expect(self.status_filter).to_be_visible()
        expect(self.status_filter.locator("option:checked")).to_have_text("Все статусы")


    def check_filter_by_priority_initial_state(self):

        expect(self.priority_filter).to_be_visible()
        expect(self.priority_filter.locator("option:checked")).to_have_text("Все приоритеты")


    def check_filter_by_status_filtered_state(self, status: str):

        expect(self.status_filter).to_be_visible()
        expect(self.status_filter.locator("option:checked")).to_have_text(status)


    def check_filter_by_priority_filtered_state(self, priority: str):

        expect(self.priority_filter).to_be_visible()
        expect(self.priority_filter.locator("option:checked")).to_have_text(priority)

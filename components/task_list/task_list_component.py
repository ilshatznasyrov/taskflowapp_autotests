import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent
from components.task_item.task_item_component import TaskItemComponent


class TaskListComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.task_list = page.get_by_test_id("tasks-list")
        self.empty_state = page.locator("//div[@class=\"empty-state\"]")


    @allure.step("Проверяем, что отображается заглушка с текстом 'Задач нет'")
    def check_visible_with_no_tasks(self):

        expect(self.task_list).to_be_visible()

        expect(self.empty_state).to_be_visible()
        expect(self.empty_state).to_contain_text("Задач нет")


    @allure.step("Проверяем наличие задачи с названием '{title}' в списке задач")
    def check_visible_with_tasks(self, title: str):

        expect(self.task_list).to_be_visible()
        expect(self.empty_state).not_to_be_visible()

        task = TaskItemComponent(self.page, title)
        task.check_visible()
        task.check_title(title)


    @allure.step("Проверяем отсутствие задачи с названием '{title}' в списке задач")
    def check_not_visible_task_in_task_list_with_tasks(self, title: str):

        expect(self.task_list).to_be_visible()
        expect(self.empty_state).not_to_be_visible()

        task = TaskItemComponent(self.page, title)
        task.check_not_visible()


    @allure.step("Проверяем статус у задачи с названием '{title}' в списке задач")
    def check_task_status(self, title: str, status: str):

        task = TaskItemComponent(self.page, title)
        task.check_status(status)


    @allure.step("Проверяем приоритет у задачи с названием '{title}' в списке задач")
    def check_task_priority(self, title: str, priority: str):

        task = TaskItemComponent(self.page, title)
        task.check_priority(priority)


    @allure.step("Проверяем, что отмечен чекбокс у задачи с названием '{title}' в списке задач")
    def check_task_checkbox_to_be_checked(self, title: str):

        expect(self.task_list).to_be_visible()
        expect(self.empty_state).not_to_be_visible()

        task = TaskItemComponent(self.page, title)
        task.check_checkbox_to_be_checked()


    @allure.step("Проверяем, что не отмечен чекбокс у задачи с названием '{title}' в списке задач")
    def check_task_checkbox_not_to_be_checked(self, title: str):

        expect(self.task_list).to_be_visible()
        expect(self.empty_state).not_to_be_visible()

        task = TaskItemComponent(self.page, title)
        task.check_checkbox_not_to_be_checked()

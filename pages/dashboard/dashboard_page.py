import allure
from playwright.sync_api import Page, expect

from components.alert.alert_component import AlertComponent
from pages.base_page import BasePage
from components.navigation.navbar_component import NavbarComponent
from components.stat_card.stat_card_component import StatCardComponent
from components.toolbar.toolbar_component import ToolbarComponent
from components.task_list.task_list_component import TaskListComponent
from components.task_item.task_item_component import TaskItemComponent
from components.task_form.task_form_component import TaskFormComponent


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)

        self.card_total_tasks = StatCardComponent(page, "total", "Всего задач")
        self.card_todo_tasks = StatCardComponent(page, "todo", "К выполнению")
        self.card_in_progress_tasks = StatCardComponent(page, "progress", "В работе")
        self.card_done_tasks = StatCardComponent(page, "done", "Выполнено")

        self.delete_btn = page.locator(".delete-btn")

        self.toolbar = ToolbarComponent(page)
        self.task_list = TaskListComponent(page)
        self.task_form = TaskFormComponent(page)

        self.alert = AlertComponent(page)


    def check_counters_with_no_tasks(self):
        self.card_total_tasks.check_visible("0")
        self.card_todo_tasks.check_visible("0")
        self.card_in_progress_tasks.check_visible("0")
        self.card_done_tasks.check_visible("0")


    def check_counters_with_tasks(self, total: str, todo: str, in_progress: str, done: str):
        self.card_total_tasks.check_visible(total)
        self.card_todo_tasks.check_visible(todo)
        self.card_in_progress_tasks.check_visible(in_progress)
        self.card_done_tasks.check_visible(done)


    def check_toolbar(self):
        self.toolbar.check_visible()


    def check_tasks_list_with_no_tasks(self):
        self.task_list.check_visible_with_no_tasks()


    def check_tasks_list_with_tasks(self, title: str):
        self.task_list.check_visible_with_tasks(title)


    def check_not_task_in_task_list_with_tasks(self, title: str):
        self.task_list.check_not_visible_task_in_task_list_with_tasks(title)


    def open_task_form(self):
        self.toolbar.click_add_task_button()


    def check_task_form(self):
        self.task_form.check_visible()


    def check_closed_task_form(self):
        self.task_form.check_not_visible()


    def close_task_form(self):
        self.task_form.click_close_form_button()


    def create_task_by_opening_form(self, title: str, description: str, status: str, priority: str):
        self.toolbar.click_add_task_button()
        self.task_form.check_visible_form_content_for_new_task()
        self.task_form.add_task(title, description, status, priority)


    def create_task_in_already_open_form(self, title: str, description: str, status: str, priority: str):
        self.task_form.check_visible_form_content_for_new_task()
        self.task_form.add_task(title, description, status, priority)


    def create_task_with_only_title(self, title: str):
        self.task_form.check_visible_form_content_for_new_task()
        self.task_form.add_task_with_default_status_and_priority(title)


    def create_task_with_spaces_in_title(self):
        self.task_form.check_visible_form_content_for_new_task()
        self.task_form.add_task_with_spaces_in_title()


    def add_task_with_not_title(self):
        self.task_form.save_form_with_not_title()


    def open_task_form_and_edit_task(self, old_title: str, title: str, description: str, status: str, priority: str):
        task_item = TaskItemComponent(self.page, old_title)
        task_item.click_task_edit_button()
        self.task_form.edit_task_and_save(title, description, status, priority)


    def open_task_form_and_edit_task_status(self, expect_title: str, status: str):
        task_item = TaskItemComponent(self.page, expect_title)
        task_item.click_task_edit_button()
        self.task_form.edit_task_status_and_save(status)


    def edit_task_and_not_save(self, old_title: str, title: str, description: str, status: str, priority: str):
        task_item = TaskItemComponent(self.page, old_title)
        task_item.click_task_edit_button()
        self.task_form.edit_task_and_not_save(title, description, status, priority)
        self.task_form.check_form_fields(title, description, status, priority)
        self.task_form.click_close_form_button()


    def check_task_editing(self, title: str, description: str, status: str, priority: str):
        task_item = TaskItemComponent(self.page, title)
        task_item.check_visible()
        task_item.check_title(title)
        task_item.click_task_edit_button()
        self.task_form.check_form_fields(title, description, status, priority)


    def open_task_form_and_check_task_status(self, expect_title: str, status: str):
        task_item = TaskItemComponent(self.page, expect_title)
        task_item.click_task_edit_button()
        self.task_form.check_task_status(status)


    def delete_task(self, expect_title: str):
        task_item = TaskItemComponent(self.page, expect_title)
        task_item.click_task_delete_button_and_confirm_deletion()
        task_item.check_not_visible()


    def cancel_delete_task(self, expect_title: str):
        task_item = TaskItemComponent(self.page, expect_title)
        task_item.click_task_delete_button_and_canceling_deletion()
        task_item.check_visible()


    @allure.step("Удаляем все задачи через UI")
    def clear_all_tasks_via_ui(self):
        while self.delete_btn.count() > 0:
            self.delete_btn.first.click()
            self.alert.check_visible_confirm_of_delete()
            self.alert.click_confirm_button_ok()
            self.alert.check_confirm_closed()
            self.alert.check_visible_alert_of_delete()
            self.alert.click_alert_button()
            self.alert.check_alert_closed()
            self.page.wait_for_timeout(300)
            
import re

import allure
from playwright.sync_api import Page, expect

from components.base_component import BaseComponent
from components.task_form.task_form_component import TaskFormComponent
from components.alert.alert_component import AlertComponent


class TaskItemComponent(BaseComponent):

    def __init__(self, page: Page, title: str):
        super().__init__(page)

        self.task_form = TaskFormComponent(page)
        self.alert = AlertComponent(page)

        self.task = (
            page.get_by_test_id("tasks-list")
            .locator(".task-item")
            .filter(has=page.locator(".task-title", has_text=title))
        )

        self.task_checkbox = self.task.locator(".task-checkbox")
        self.task_title = self.task.locator(".task-title")
        self.task_description = self.task.locator(".task-description")
        self.task_status = self.task.locator(".task-status")
        self.task_priority = self.task.locator(".task-priority")
        self.edit_btn = self.task.locator(".edit-btn")
        self.delete_btn = self.task.locator(".delete-btn")


    def check_visible(self):

        expect(self.task).to_be_visible()


    @allure.step("Проверяем, что задача не отображается")
    def check_not_visible(self):

        expect(self.task).not_to_be_visible()


    def check_title(self, expected_title: str):

        expect(self.task_title).to_have_text(expected_title)


    def check_description(self, expected_description: str):

        expect(self.task_description).to_have_text(expected_description)


    def check_status(self, expected_status: str):

        expect(self.task_status).to_have_class(re.compile(f".*status-{expected_status}.*"))


    def check_priority(self, expected_priority: str):

        expect(self.task_priority).to_have_class(re.compile(f".*priority-{expected_priority}.*"))


    def check_checkbox_to_be_checked(self):

        expect(self.task_checkbox).to_be_checked()


    def check_checkbox_not_to_be_checked(self):

        expect(self.task_checkbox).not_to_be_checked()


    @allure.step("Нажимаем на кнопку 'Редактировать' у задачи")
    def click_task_edit_button(self):

        expect(self.edit_btn).to_be_visible()
        self.edit_btn.click()
        self.task_form.check_visible()


    @allure.step("Нажимаем на кнопку 'Удалить' у задачи и подтверждаем удаление")
    def click_task_delete_button_and_confirm_deletion(self):

        expect(self.delete_btn).to_be_visible()
        self.delete_btn.click()
        self.alert.check_visible_confirm_of_delete()
        self.alert.click_confirm_button_ok()
        self.alert.check_confirm_closed()
        self.alert.check_visible_alert_of_delete()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Нажимаем на кнопку 'Удалить' у задачи и отменяем удаление")
    def click_task_delete_button_and_canceling_deletion(self):

        expect(self.delete_btn).to_be_visible()
        self.delete_btn.click()
        self.alert.check_visible_confirm_of_delete()
        self.alert.click_confirm_button_cancel()
        self.alert.check_confirm_closed()

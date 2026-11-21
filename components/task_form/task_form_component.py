import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent
from components.alert.alert_component import AlertComponent


class TaskFormComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.alert = AlertComponent(page)

        self.task_modal_container = page.locator("#taskModal")
        self.form_title = page.get_by_test_id("modal-title")
        self.label_task_title = page.locator("//label[@for=\"taskTitle\"]")
        self.title_input = page.get_by_test_id("task-title-input")
        self.label_task_description = page.locator("//label[@for=\"taskDescription\"]")
        self.description_input = page.get_by_test_id("task-description-input")
        self.label_task_status = page.locator("//label[@for=\"taskStatus\"]")
        self.status_select = page.get_by_test_id("task-status-select")
        self.label_task_priority = page.locator("//label[@for=\"taskPriority\"]")
        self.priority_select = page.get_by_test_id("task-priority-select")
        self.save_button = page.get_by_test_id("save-task-button")
        self.close_button = page.get_by_test_id("close-modal")


    @allure.step("Проверяем отображение контейнера формы на странице")
    def check_visible(self):

        expect(self.task_modal_container).to_be_visible()


    @allure.step("Проверяем отображение содержимого формы")
    def check_visible_form_content(self):

        expect(self.label_task_title).to_be_visible()
        expect(self.label_task_title).to_have_text("Заголовок *")
        expect(self.title_input).to_be_visible()

        expect(self.label_task_description).to_be_visible()
        expect(self.label_task_description).to_have_text("Описание")
        expect(self.description_input).to_be_visible()

        expect(self.label_task_status).to_be_visible()
        expect(self.label_task_status).to_have_text("Статус")
        expect(self.status_select).to_be_visible()

        expect(self.label_task_priority).to_be_visible()
        expect(self.label_task_priority).to_have_text("Приоритет")
        expect(self.priority_select).to_be_visible()

        expect(self.save_button).to_be_visible()
        expect(self.save_button).to_have_text("Сохранить")


    @allure.step("Проверяем отображение содержимого формы для новой задачи")
    def check_visible_form_content_for_new_task(self):

        expect(self.form_title).to_be_visible()
        expect(self.form_title).to_have_text("Новая задача")

        expect(self.label_task_title).to_be_visible()
        expect(self.label_task_title).to_have_text("Заголовок *")

        expect(self.title_input).to_be_visible()
        expect(self.title_input).to_have_attribute(
            "placeholder", "Введите заголовок задачи"
        )

        expect(self.label_task_description).to_be_visible()
        expect(self.label_task_description).to_have_text("Описание")

        expect(self.description_input).to_be_visible()
        expect(self.description_input).to_have_attribute(
            "placeholder", "Введите описание задачи"
        )

        expect(self.label_task_status).to_be_visible()
        expect(self.label_task_status).to_have_text("Статус")

        expect(self.status_select).to_be_visible()
        expect(self.status_select.locator("option:checked")).to_have_text("К выполнению")

        expect(self.label_task_priority).to_be_visible()
        expect(self.label_task_priority).to_have_text("Приоритет")

        expect(self.priority_select).to_be_visible()
        expect(self.priority_select.locator("option:checked")).to_have_text("Низкий")

        expect(self.save_button).to_be_visible()
        expect(self.save_button).to_have_text("Сохранить")


    @allure.step("Проверяем, что форма не отображается")
    def check_not_visible(self):

        expect(self.label_task_title).not_to_be_visible()
        expect(self.title_input).not_to_be_visible()

        expect(self.label_task_description).not_to_be_visible()
        expect(self.description_input).not_to_be_visible()

        expect(self.label_task_status).not_to_be_visible()
        expect(self.status_select).not_to_be_visible()

        expect(self.label_task_priority).not_to_be_visible()
        expect(self.priority_select).not_to_be_visible()

        expect(self.save_button).not_to_be_visible()


    @allure.step("Заполняем форму задачи и сохраняем")
    def add_task(self, title: str, description: str, status: str, priority: str):

        self.title_input.fill(title)
        self.description_input.fill(description)
        self.status_select.select_option(status)
        self.priority_select.select_option(priority)
        self.save_button.click()
        self.alert.check_visible_alert_of_creation()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Заполняем только название задачи в форме и сохраняем")
    def add_task_with_default_status_and_priority(self, title: str):

        self.title_input.fill(title)
        self.save_button.click()
        self.alert.check_visible_alert_of_creation()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Заполняем пробелами название задачи в форме и сохраняем")
    def add_task_with_spaces_in_title(self):
        self.title_input.fill("   ")
        self.save_button.click()
        self.alert.check_visible_alert_not_title()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Кликаем на крестик в форме задачи")
    def click_close_form_button(self):

        self.close_button.click()
        expect(self.title_input).not_to_be_visible()


    @allure.step("Пытаемся сохранить форму без заголовка и проверяем что форма не закрылась")
    def save_form_with_not_title(self):

        self.title_input.clear()
        self.save_button.click()

        expect(self.title_input).to_be_visible()
        expect(self.title_input).to_have_text("")
        expect(self.save_button).to_be_visible()


    @allure.step("Редактируем задачу и сохраняем")
    def edit_task_and_save(self, title: str, description: str, status: str, priority: str):

        self.title_input.clear()
        self.description_input.clear()
        self.title_input.fill(title)
        self.description_input.fill(description)
        self.status_select.select_option(status)
        self.priority_select.select_option(priority)

        expect(self.title_input).to_be_visible()
        expect(self.title_input).to_have_value(title)
        expect(self.description_input).to_be_visible()
        expect(self.description_input).to_have_value(description)

        self.save_button.click()
        self.alert.check_visible_alert_of_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Редактируем статус задачи и сохраняем")
    def edit_task_status_and_save(self, status: str):

        expect(self.status_select).to_be_visible()
        self.status_select.select_option(status)
        self.save_button.click()
        self.alert.check_visible_alert_of_update()
        self.alert.click_alert_button()
        self.alert.check_alert_closed()


    @allure.step("Редактируем задачу и не сохраняем")
    def edit_task_and_not_save(self, title: str, description: str, status: str, priority: str):

        self.title_input.clear()
        self.description_input.clear()
        self.title_input.fill(title)
        self.description_input.fill(description)
        self.status_select.select_option(status)
        self.priority_select.select_option(priority)


    @allure.step("Проверяем содержимое полей формы")
    def check_form_fields(self, title: str, description: str, status: str, priority: str):

        expect(self.title_input).to_be_visible()
        expect(self.title_input).to_have_value(title)
        expect(self.description_input).to_be_visible()
        expect(self.description_input).to_have_value(description)
        expect(self.status_select).to_be_visible()
        expect(self.status_select).to_have_value(status)
        expect(self.priority_select).to_be_visible()
        expect(self.priority_select).to_have_value(priority)


    @allure.step("Проверяем статус задачи в форме")
    def check_task_status(self, status: str):

        expect(self.status_select).to_be_visible()
        expect(self.status_select.locator("option:checked")).to_have_text(status)


    @allure.step("Проверяем приоритет задачи в форме")
    def check_task_priority(self, priority: str):

        expect(self.priority_select).to_be_visible()
        expect(self.priority_select.locator("option:checked")).to_have_text(priority)

import uuid
import pytest
import allure
from allure_commons.types import Severity
from pages.dashboard.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.task_form
@allure.tag("web")
@allure.feature("Задачи")
class TaskFormBase:
    """Базовый класс формы задачи"""

    @allure.title("Проверка отображения всех полей формы")
    @allure.severity(Severity.NORMAL)
    def test_form_fields_display(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
            dashboard_page.task_form.check_visible_form_content()


    @allure.title("Проверка закрытия формы по крестику")
    @allure.severity(Severity.NORMAL)
    def test_close_form_by_cross(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
            dashboard_page.task_form.check_visible_form_content()
        with allure.step("Закрываем форму задачи по крестику"):
            dashboard_page.close_task_form()
        with allure.step("Проверяем, что форма закрылась"):
            dashboard_page.check_closed_task_form()


    @allure.title("Проверка создания задачи c заголовком, состоящим из пробелов")
    @allure.severity(Severity.NORMAL)
    def test_create_task_with_spaces_in_title(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу c заголовком из пробелов"):
            dashboard_page.create_task_with_spaces_in_title()
        with allure.step("Проверяем, что форма не сохранилась и не закрылась"):
            dashboard_page.check_task_form()


    @allure.title("Проверка валидации формы при создании/редактировании задачи без заголовка")
    @allure.severity(Severity.NORMAL)
    def test_form_validation_without_title(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
            dashboard_page.task_form.check_visible_form_content()
        with allure.step("Проверяем создание задачи без заголовка"):
            dashboard_page.task_form.save_form_with_not_title()
            dashboard_page.task_form.check_visible_form_content()


class TestTaskCreation(TaskFormBase):
    """Тесты создания задачи"""

    @pytest.mark.smoke
    @allure.title("Создание задачи с заполнением всех полей")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.parametrize(
         "title, description, status, priority",
         [
            ("first",
            "This is a first test task",
             "todo",
             "medium",
             ),
            ("second",
             "This is a second test task",
             "in-progress",
             "low",
             ),
            ("third",
             "This is a third test task",
             "done",
             "high",
             ),
        ]
    )
    def test_create_task_with_all_fields(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            title: str,
            description: str,
            status: str,
            priority: str,
    ):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.create_task_in_already_open_form(title, description, status, priority)
        with allure.step("Проверяем отображение созданной задачи в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(title)


    @allure.title("Создание задачи только с заголовком")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "title",
        [
            "normal",
            "№()@#$%&-+!",
            "123",
        ]
    )
    def test_create_task_with_title_only(self, dashboard_page: DashboardPage, user_authenticated: dict, title: str):

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу с заполнением только заголовка в форме задачи"):
            dashboard_page.create_task_with_only_title(title)
        with allure.step("Проверяем отображение созданной задачи в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(title)


class TestTaskEditing(TaskFormBase):
    """Тесты редактирования задачи"""

    @pytest.mark.smoke
    @allure.title("Редактирование задачи и сохранение изменений")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.parametrize(
        "title, description, status, priority",
        [
            ("first",
             "This is a first test task",
             "done",
             "high",
             ),
            ("second",
             "This is a second test task",
             "todo",
             "medium",
             ),
            ("third",
             "This is a third test task",
             "in-progress",
             "low",
             ),
        ]
    )
    def test_edit_task_and_save(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            title: str,
            description: str,
            status: str,
            priority: str,
    ):

        unique_id = uuid.uuid4().hex[:6]

        initial_title = f"init_{unique_id}_{title}"
        updated_title = f"upd_{unique_id}_{title}"

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.create_task_in_already_open_form(initial_title, "Old description", "todo", "low")
        with allure.step("Открываем задачу на редактирование и изменяем содержимое полей в форме задачи"):
            dashboard_page.open_task_form_and_edit_task(initial_title, updated_title, description, status, priority)
        with allure.step("Открываем форму задачи и проверяем, что изменения успешно сохранились"):
            dashboard_page.check_task_editing(updated_title, description, status, priority)
        with allure.step("Закрываем форму задачи"):
            dashboard_page.close_task_form()


    @allure.title("Проверка предзаполнения формы данными задачи")
    @allure.severity(Severity.NORMAL)
    def test_form_prefilled_with_task_data(self, dashboard_page: DashboardPage, user_authenticated: dict):

        unique_id = uuid.uuid4().hex[:6]

        expected_title = f"expected_title_{unique_id}"
        expected_description = "my description"
        expected_status = "todo"
        expected_priority = "low"

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.create_task_in_already_open_form(expected_title, expected_description, expected_status, expected_priority)
        with allure.step("Открываем задачу на редактирование и проверяем предзаполнение формы данными задачи"):
            dashboard_page.check_task_editing(expected_title, expected_description, expected_status, expected_priority)
        with allure.step("Закрываем форму задачи"):
            dashboard_page.close_task_form()


    @allure.title("Отмена редактирования задачи")
    @allure.severity(Severity.NORMAL)
    def test_cancel_task_editing(self, dashboard_page: DashboardPage, user_authenticated: dict):

        unique_id = uuid.uuid4().hex[:6]

        expected_title = f"expected_title_{unique_id}"
        expected_description = "my description"
        expected_status = "todo"
        expected_priority = "low"

        updated_title = f"upd_title_{unique_id}"
        updated_description = "upd description"
        updated_status = "in-progress"
        updated_priority = "high"

        with allure.step("Проверяем, что отображается страница дашборда с пустыми счетчиками задач"):
            dashboard_page.check_tasks_list_with_no_tasks()
        with allure.step("Открываем форму задачи"):
            dashboard_page.open_task_form()
        with allure.step("Проверяем отображение формы задачи"):
            dashboard_page.check_task_form()
        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.create_task_in_already_open_form(expected_title, expected_description,
                                                                       expected_status, expected_priority)
        with allure.step("Открываем задачу на редактирование и изменяем содержимое полей в форме задачи"):
            dashboard_page.edit_task_and_not_save(expected_title, updated_title, updated_description, updated_status, updated_priority)
        with allure.step("Открываем задачу на редактирование и проверяем, что данные задачи в форме остались прежними"):
            dashboard_page.check_task_editing(expected_title, expected_description, expected_status,
                                                         expected_priority)
        with allure.step("Закрываем форму задачи"):
            dashboard_page.close_task_form()

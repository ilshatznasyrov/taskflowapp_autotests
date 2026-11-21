import uuid

import pytest
import allure
from allure_commons.types import Severity
from pages.dashboard.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.task_list
@allure.tag("web")
@allure.feature("Список задач")
class TestTaskList:

    @allure.title("Проверка статуса у задачи в списке задач")
    @allure.severity(Severity.NORMAL)
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
    def test_displaying_status_of_task_in_task_list(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            title: str,
            description: str,
            status: str,
            priority: str,
    ):

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.check_task_form()
            dashboard_page.create_task_in_already_open_form(title, description, status, priority)
        with allure.step("Проверяем отображение созданной задачи в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(title)
        with allure.step("Проверяем статус созданной задачи в списке задач"):
            dashboard_page.task_list.check_task_status(title, status)


    @allure.title("Проверка приоритета у задачи в списке задач")
    @allure.severity(Severity.NORMAL)
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
    def test_displaying_priority_of_task_in_task_list(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            title: str,
            description: str,
            status: str,
            priority: str,
    ):

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.check_task_form()
            dashboard_page.create_task_in_already_open_form(title, description, status, priority)
        with allure.step("Проверяем отображение созданной задачи в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(title)
        with allure.step("Проверяем приоритет созданной задачи в списке задач"):
            dashboard_page.task_list.check_task_priority(title, priority)


    @pytest.mark.not_parallel
    @allure.title("Проверка чекбокса у задач")
    @allure.severity(Severity.NORMAL)
    def test_checkbox_to_be_checked(self, dashboard_page: DashboardPage, user_authenticated: dict):

        tasks = [
            ("first", "This is a first test task", "todo", "medium"),
            ("second", "This is a second test task", "in-progress", "low"),
            ("third", "This is a third test task", "done", "high"),
        ]

        expected_counters = [
            ("1", "1", "0", "0"),
            ("2", "1", "1", "0"),
            ("3", "1", "1", "1"),
        ]

        step = 1

        with allure.step("Создаем 3 задачи с разными статусами и приоритетом"):
            for task, counters in zip(tasks, expected_counters):
                title, description, status, priority = task
                with allure.step(f"Создаем задачу {step}"):
                    dashboard_page.create_task_by_opening_form(title, description, status, priority)
                    step += 1
                with allure.step("Проверяем, что созданная задача появилась в списке задач"):
                    dashboard_page.check_tasks_list_with_tasks(title)
        with allure.step(
                "Проверяем, что у задачи со статусом 'Выполнено' отмечен чекбокс, а у остальных задач не отмечен"):
            dashboard_page.task_list.check_task_status("third", "done")
            dashboard_page.task_list.check_task_checkbox_to_be_checked("third")
            dashboard_page.task_list.check_task_checkbox_not_to_be_checked("second")
            dashboard_page.task_list.check_task_checkbox_not_to_be_checked("first")


    @pytest.mark.smoke
    @allure.title("Проверка удаления задачи")
    @allure.severity(Severity.CRITICAL)
    def test_task_deletion_removes_from_list(self, dashboard_page: DashboardPage, user_authenticated: dict):

        unique_id = uuid.uuid4().hex[:6]
        expect_title = f"task_{unique_id}"

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.create_task_in_already_open_form(expect_title, "This is a test task", "todo",
                                                                       "low")
        with allure.step("Проверяем, что созданная задача появилась в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(expect_title)
        with allure.step("Удаляем задачу и проверяем, что задача пропала"):
            dashboard_page.delete_task(expect_title)

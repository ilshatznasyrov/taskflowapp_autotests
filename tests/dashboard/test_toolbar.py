import uuid

import pytest
import allure
from allure_commons.types import Severity
from pages.dashboard.dashboard_page import DashboardPage



@pytest.mark.regression
@pytest.mark.toolbar
@allure.tag("web")
@allure.feature("Тулбар")
class TestToolbar:


    @pytest.mark.smoke
    @pytest.mark.not_parallel
    @allure.title("Проверка валидного поиска задачи")
    @allure.severity(Severity.CRITICAL)
    def test_search_task(self, dashboard_page: DashboardPage, user_authenticated: dict):

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
        with allure.step("Выполняем поиск задачи по тексту 'second'"):
            dashboard_page.toolbar.check_search_input()
            dashboard_page.toolbar.fill_text_in_search("second")
            dashboard_page.toolbar.check_filled_search_value_saved_in_input_field("second")
        with allure.step("Проверяем, что искомая задача найдена и остальные задачи не отображаются"):
            dashboard_page.check_tasks_list_with_tasks("second")
            dashboard_page.check_not_task_in_task_list_with_tasks("first")
            dashboard_page.check_not_task_in_task_list_with_tasks("third")


    @pytest.mark.not_parallel
    @allure.title("Проверка фильтрации задач по статусу")
    @allure.severity(Severity.NORMAL)
    def test_filter_tasks_by_status(self, dashboard_page: DashboardPage, user_authenticated: dict):

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
        with allure.step("Фильтруем список задач по статусу done"):
            dashboard_page.toolbar.check_filter_by_status_initial_state()
            dashboard_page.toolbar.select_filter_by_status("done")
            dashboard_page.toolbar.check_filter_by_status_filtered_state("Выполнено")
        with allure.step("Проверяем, что задача соответствующая фильтру найдена и остальные задачи не отображаются"):
            dashboard_page.check_tasks_list_with_tasks("third")
            dashboard_page.task_list.check_task_status("third", "done")
            dashboard_page.check_not_task_in_task_list_with_tasks("first")
            dashboard_page.check_not_task_in_task_list_with_tasks("second")


    @pytest.mark.not_parallel
    @allure.title("Проверка фильтрации задач по приоритету")
    @allure.severity(Severity.NORMAL)
    def test_filter_tasks_by_priority(self, dashboard_page: DashboardPage, user_authenticated: dict):

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
        with allure.step("Фильтруем список задач по приоритету medium"):
            dashboard_page.toolbar.check_filter_by_priority_initial_state()
            dashboard_page.toolbar.select_filter_by_priority("medium")
            dashboard_page.toolbar.check_filter_by_priority_filtered_state("Средний")
        with allure.step("Проверяем, что задача соответствующая фильтру найдена и остальные задачи не отображаются"):
            dashboard_page.check_tasks_list_with_tasks("first")
            dashboard_page.task_list.check_task_priority("first", "medium")
            dashboard_page.check_not_task_in_task_list_with_tasks("third")
            dashboard_page.check_not_task_in_task_list_with_tasks("second")


    @pytest.mark.not_parallel
    @allure.title("Проверка очистки поля поиска")
    @allure.severity(Severity.NORMAL)
    def test_clear_search_field(self, dashboard_page: DashboardPage, user_authenticated: dict):

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
        with allure.step("Выполняем поиск задачи по тексту 'second'"):
            dashboard_page.toolbar.check_search_input()
            dashboard_page.toolbar.fill_text_in_search("second")
            dashboard_page.toolbar.check_filled_search_value_saved_in_input_field("second")
        with allure.step("Проверяем, что искомая задача найдена и остальные задачи не отображаются"):
            dashboard_page.check_tasks_list_with_tasks("second")
            dashboard_page.check_not_task_in_task_list_with_tasks("first")
            dashboard_page.check_not_task_in_task_list_with_tasks("third")
        with allure.step("Очищаем поиск"):
            dashboard_page.toolbar.clear_search()
        with allure.step("Проверяем, что все задачи отображаются"):
            dashboard_page.check_tasks_list_with_tasks("first")
            dashboard_page.check_tasks_list_with_tasks("second")
            dashboard_page.check_tasks_list_with_tasks("third")


    @pytest.mark.not_parallel
    @allure.title("Проверка комбинирования фильтрации по статусу и приоритету")
    @allure.severity(Severity.NORMAL)
    def test_combined_filter_status_and_priority(self, dashboard_page: DashboardPage, user_authenticated: dict):

        tasks = [
            ("first", "This is a first test task", "todo", "medium"),
            ("second", "This is a second test task", "in-progress", "medium"),
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
        with allure.step("Фильтруем список задач по приоритету medium"):
            dashboard_page.toolbar.check_filter_by_priority_initial_state()
            dashboard_page.toolbar.select_filter_by_priority("medium")
            dashboard_page.toolbar.check_filter_by_priority_filtered_state("Средний")
        with allure.step("Проверяем, что в списке отображаются задачи соответствующие фильтру, а не соответствующая не отображается"):
            dashboard_page.check_tasks_list_with_tasks("first")
            dashboard_page.check_tasks_list_with_tasks("second")
            dashboard_page.task_list.check_task_priority("first", "medium")
            dashboard_page.task_list.check_task_priority("second", "medium")
            dashboard_page.check_not_task_in_task_list_with_tasks("third")
        with allure.step("Фильтруем список задач по статусу todo"):
            dashboard_page.toolbar.check_filter_by_status_initial_state()
            dashboard_page.toolbar.select_filter_by_status("todo")
            dashboard_page.toolbar.check_filter_by_status_filtered_state("К выполнению")
        with allure.step("Проверяем, что в списке отображается задача соответствующая обоим фильтрам и остальные задачи не отображаются"):
            dashboard_page.check_tasks_list_with_tasks("first")
            dashboard_page.task_list.check_task_status("first", "todo")
            dashboard_page.task_list.check_task_priority("first", "medium")
            dashboard_page.check_not_task_in_task_list_with_tasks("second")
            dashboard_page.check_not_task_in_task_list_with_tasks("third")


    @pytest.mark.not_parallel
    @allure.title("Проверка отображения пустого результата поиска")
    @allure.severity(Severity.NORMAL)
    def test_empty_search_results(self, dashboard_page: DashboardPage, user_authenticated: dict):

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

        empty_search = "empty_search"

        step = 1

        with allure.step("Создаем 3 задачи с разными статусами и приоритетом"):
            for task, counters in zip(tasks, expected_counters):
                title, description, status, priority = task
                with allure.step(f"Создаем задачу {step}"):
                    dashboard_page.create_task_by_opening_form(title, description, status, priority)
                    step += 1
                with allure.step("Проверяем, что созданная задача появилась в списке задач"):
                    dashboard_page.check_tasks_list_with_tasks(title)
        with allure.step(f"Выполняем поиск задачи по тексту '{empty_search}'"):
            dashboard_page.toolbar.check_search_input()
            dashboard_page.toolbar.fill_text_in_search(empty_search)
            dashboard_page.toolbar.check_filled_search_value_saved_in_input_field(empty_search)
        with allure.step("Проверяем, что задачи с искомым текстом не найдены"):
            dashboard_page.check_tasks_list_with_no_tasks()


    @allure.title("Проверка поиска по несуществующим или невалидным запросам")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "search_query",
        [
            "   ",
            "№()@#$%&-+!",
            "123",
            "<script>alert(1)</script>",
        ]
    )
    def test_search_with_no_results(self, dashboard_page: DashboardPage, user_authenticated: dict, search_query: str):

        unique_id = uuid.uuid4().hex[:6]

        expected_title = f"expected_title_{unique_id}"
        expected_description = "my description"
        expected_status = "todo"
        expected_priority = "low"

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.check_task_form()
            dashboard_page.create_task_in_already_open_form(expected_title, expected_description, expected_status, expected_priority)
        with allure.step(f"Выполняем поиск по тексту '{search_query}'"):
            dashboard_page.toolbar.check_search_input()
            dashboard_page.toolbar.fill_text_in_search(search_query)
            dashboard_page.toolbar.check_filled_search_value_saved_in_input_field(search_query)
        with allure.step("Проверяем, что результаты поиска отсутствуют"):
            dashboard_page.check_tasks_list_with_no_tasks()

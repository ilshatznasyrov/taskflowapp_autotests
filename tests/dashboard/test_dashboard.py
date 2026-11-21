import uuid

import pytest
import allure
from allure_commons.types import Severity
from pages.dashboard.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.dashboard
@allure.tag("web")
@allure.feature("Статистика дашборда")
class TestDashboard:

    @allure.title("Проверка отображения статистики дашборда без задач")
    @allure.severity(Severity.NORMAL)
    def test_dashboard_displaying_with_no_tasks(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что все счетчики статистики показывают '0'"):
            dashboard_page.check_counters_with_no_tasks()
        with allure.step("Проверяем, что список задач пустой"):
            dashboard_page.check_tasks_list_with_no_tasks()


    @pytest.mark.smoke
    @pytest.mark.not_parallel
    @allure.title("Проверка отображения статистики дашборда с задачами")
    @allure.severity(Severity.CRITICAL)
    def test_dashboard_displaying_with_tasks(self, dashboard_page: DashboardPage, user_authenticated: dict):

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

        with allure.step("Создаем 3 задачи с разными статусами и приоритетом и проверяем корректность обновления счетчиков статистики"):
            for task, counters in zip(tasks, expected_counters):
                title, description, status, priority = task
                with allure.step(f"Создаем задачу {step}"):
                    dashboard_page.create_task_by_opening_form(title, description, status, priority)
                    step += 1
                with allure.step("Проверяем, что созданная задача появилась в списке задач"):
                    dashboard_page.check_tasks_list_with_tasks(title)
                with allure.step("Проверяем, что счетчики статистики обновились корректно"):
                    dashboard_page.check_counters_with_tasks(*counters)


    @pytest.mark.smoke
    @allure.title("Проверка обновления статистики дашборда после редактирования задачи")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.parametrize(
        "target_status, total_counter, todo_counter, in_progress_counter, done_counter",
        [
            ("todo", "1", "1", "0", "0"),
            ("in-progress", "1", "0", "1", "0"),
            ("done", "1", "0", "0", "1"),
        ]
    )
    def test_dashboard_displaying_after_editing_task(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            target_status: str,
            total_counter: str,
            todo_counter: str,
            in_progress_counter: str,
            done_counter: str
    ):

        unique_id = uuid.uuid4().hex[:6]
        expect_title = f"task_{unique_id}"

        if target_status == "todo":
            initial_status = "in-progress"
        else:
            initial_status = "todo"

        with allure.step(f"Создаем задачу с начальным статусом '{initial_status}'"):
            dashboard_page.open_task_form()
            dashboard_page.create_task_in_already_open_form(expect_title, "This is a test task", initial_status, "low")
        with allure.step("Проверяем, что созданная задача появилась в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(expect_title)
            dashboard_page.task_list.check_task_status(expect_title, initial_status)
        with allure.step("Открываем задачу на редактирование и изменяем статус в форме задачи"):
            dashboard_page.open_task_form_and_edit_task_status(expect_title, target_status)
            dashboard_page.task_list.check_task_status(expect_title, target_status)
        with allure.step("Проверяем, что счетчики статистики обновились корректно"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter, done_counter)


    @pytest.mark.smoke
    @allure.title("Проверка обновления статистики дашборда после удаления задачи")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.parametrize(
        "status, total_counter, todo_counter, in_progress_counter, done_counter",
        [
            ("todo", "1", "1", "0", "0"),
            ("in-progress", "1", "0", "1", "0"),
            ("done", "1", "0", "0", "1"),
        ]
    )
    def test_dashboard_displaying_after_task_deletion(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            status: str,
            total_counter: str,
            todo_counter: str,
            in_progress_counter: str,
            done_counter: str
    ):

        unique_id = uuid.uuid4().hex[:6]
        expect_title = f"task_{unique_id}"

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.create_task_in_already_open_form(expect_title, "This is a test task", "todo",
                                                                       "low")
        with allure.step("Проверяем, что созданная задача появилась в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(expect_title)
        with allure.step("Открываем задачу на редактирование и изменяем статус в форме задачи"):
            dashboard_page.open_task_form_and_edit_task_status(expect_title, status)
            dashboard_page.task_list.check_task_status(expect_title, status)
        with allure.step("Проверяем, что счетчики статистики обновились корректно"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter,
                                                                done_counter)
        with allure.step("Удаляем задачу и проверяем, что задача пропала"):
            dashboard_page.delete_task(expect_title)
        with allure.step("Проверяем, что счетчики статистики обновились корректно"):
            dashboard_page.check_counters_with_tasks(total="0", todo="0", in_progress="0", done="0")


    @allure.title("Проверка отображения статистики дашборда с задачей после перезагрузки страницы")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "status, total_counter, todo_counter, in_progress_counter, done_counter",
        [
            ("todo", "1", "1", "0", "0"),
            ("in-progress", "1", "0", "1", "0"),
            ("done", "1", "0", "0", "1"),
        ]
    )
    def test_dashboard_displaying_statistics_counters_after_reload(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            status: str,
            total_counter: str,
            todo_counter: str,
            in_progress_counter: str,
            done_counter: str
    ):

        unique_id = uuid.uuid4().hex[:6]
        expect_title = f"task_{unique_id}"

        with allure.step("Создаем задачу с заполнением всех полей формы задачи"):
            dashboard_page.open_task_form()
            dashboard_page.create_task_in_already_open_form(expect_title, "This is a test task", "todo",
                                                                       "low")
        with allure.step("Проверяем, что созданная задача появилась в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(expect_title)
        with allure.step("Открываем задачу на редактирование и изменяем статус в форме задачи"):
            dashboard_page.open_task_form_and_edit_task_status(expect_title, status)
            dashboard_page.task_list.check_task_status(expect_title, status)
        with allure.step("Проверяем, что счетчики статистики обновились корректно"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter,
                                                                done_counter)
        with allure.step("Перезагружаем страницу"):
            dashboard_page.page.reload()
            dashboard_page.navbar.check_visible_logo()
        with allure.step("Проверяем, что счетчики статистики не поменялись после перезагрузки страницы"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter,
                                                                done_counter)


    @allure.title("Проверка отображения статистики дашборда с задачей после отмены удаления задачи")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "target_status, total_counter, todo_counter, in_progress_counter, done_counter",
        [
            ("todo", "1", "1", "0", "0"),
            ("in-progress", "1", "0", "1", "0"),
            ("done", "1", "0", "0", "1"),
        ]
    )
    def test_dashboard_displaying_after_cancel_task_deletion(
            self,
            dashboard_page: DashboardPage,
            user_authenticated: dict,
            target_status: str,
            total_counter: str,
            todo_counter: str,
            in_progress_counter: str,
            done_counter: str
    ):

        unique_id = uuid.uuid4().hex[:6]
        expect_title = f"task_{unique_id}"

        if target_status == "todo":
            initial_status = "in-progress"
        else:
            initial_status = "todo"

        with allure.step(f"Создаем задачу с начальным статусом '{initial_status}'"):
            dashboard_page.open_task_form()
            dashboard_page.create_task_in_already_open_form(expect_title, "This is a test task", initial_status,
                                                                       "low")
        with allure.step("Проверяем, что созданная задача появилась в списке задач"):
            dashboard_page.check_tasks_list_with_tasks(expect_title)
        with allure.step("Открываем задачу на редактирование и изменяем статус в форме задачи"):
            dashboard_page.open_task_form_and_edit_task_status(expect_title, target_status)
            dashboard_page.task_list.check_task_status(expect_title, target_status)
        with allure.step("Проверяем, что счетчики статистики обновились корректно"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter,
                                                                done_counter)
        with allure.step("Вызываем окно удаления задачи, отменяем удаление и проверяем, что задача не пропала"):
            dashboard_page.cancel_delete_task(expect_title)
        with allure.step("Проверяем, что счетчики статистики остались прежними"):
            dashboard_page.check_counters_with_tasks(total_counter, todo_counter, in_progress_counter,
                                                                done_counter)

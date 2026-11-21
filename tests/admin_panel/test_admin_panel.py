import uuid

import allure
import pytest
from allure_commons.types import Severity
from pages.admin_panel.admin_panel_page import AdminPage


@pytest.mark.regression
@pytest.mark.admin_panel
@allure.tag("web")
@allure.feature("Админка")
class TestAdminPanel:


    @pytest.mark.smoke
    @pytest.mark.stat_counters
    @pytest.mark.not_parallel
    @allure.title("Проверка счетчиков статистики пользователей")
    @allure.severity(Severity.CRITICAL)
    def test_statistics_display_correct_counts(self, logged_in_admin_page: AdminPage):

        with allure.step("Проверяем отображение панели администратора"):
            logged_in_admin_page.check_visible()
        with allure.step("Проверяем счетчики статистики пользователей"):
            counters = logged_in_admin_page.get_current_counters()
            assert counters["total"] == 3, "Общее число пользователей должно быть 3"
            assert counters["active"] == 2, "Число активных пользователей должно быть 2"
            assert counters["blocked"] == 1, "Число заблокированных пользователей должно быть 1"
            assert counters["admin"] == 1, "Число админов должно быть 1"


    @pytest.mark.smoke
    @pytest.mark.stat_counters
    @pytest.mark.not_parallel
    @allure.title("Проверка блокировки пользователя и корректное обновление счетчиков статистики после блокировки")
    @allure.severity(Severity.CRITICAL)
    def test_statistics_update_after_blocking_user(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
            counters_before = logged_in_admin_page.get_current_counters()
        with allure.step(f"Блокируем пользователя с именем '{temp_user_name}'"):
            logged_in_admin_page.blocking_user(temp_user_name)
        with allure.step("Проверяем счетчики статистики пользователей"):
            counters_after = logged_in_admin_page.get_current_counters()
            assert counters_after["total"] == counters_before["total"], "Общее число пользователей не должно меняться"
            assert counters_after["active"] == counters_before["active"] - 1, "Число активных пользователей должно стать на 1 меньше"
            assert counters_after["blocked"] == counters_before["blocked"] + 1, "Число заблокированных должно стать на 1 больше"
            assert counters_after["admin"] == counters_before["admin"], "Число админов не должно меняться"


    @pytest.mark.smoke
    @pytest.mark.stat_counters
    @pytest.mark.not_parallel
    @allure.title("Проверка разблокировки пользователя и корректное обновление счетчиков статистики после разблокировки")
    @allure.severity(Severity.CRITICAL)
    def test_statistics_update_after_unblock_user(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Блокируем пользователя с именем '{temp_user_name}'"):
            logged_in_admin_page.blocking_user(temp_user_name)
            counters_before = logged_in_admin_page.get_current_counters()
        with allure.step("Разблокируем пользователя и проверяем, что статус пользователя сменился на 'Активен'"):
            logged_in_admin_page.unblocking_user(temp_user_name)
        with allure.step("Проверяем счетчики статистики пользователей"):
            counters_after = logged_in_admin_page.get_current_counters()
            assert counters_after["total"] == counters_before["total"], "Общее число пользователей не должно меняться"
            assert counters_after["active"] == counters_before["active"] + 1, "Число активных пользователей должно стать на 1 больше"
            assert counters_after["blocked"] == counters_before["blocked"] - 1, "Число заблокированных должно стать на 1 меньше"
            assert counters_after["admin"] == counters_before["admin"], "Число админов не должно меняться"


    @pytest.mark.stat_counters
    @pytest.mark.not_parallel
    @allure.title("Проверка счетчиков статистики после регистрации нового пользователя")
    @allure.severity(Severity.NORMAL)
    def test_statistics_update_after_creating_user(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Получаем нового зарегистрированного пользователя через фикстуру"):
            logged_in_admin_page.check_user_in_userlist(temp_user_name)
        with allure.step("Проверяем счетчики статистики пользователей"):
            counters = logged_in_admin_page.get_current_counters()
            assert counters["total"] == 4, "Общее число пользователей должно стать 4"
            assert counters["active"] == 3, "Число активных пользователей должно стать 3"
            assert counters["blocked"] == 1, "Число заблокированных пользователей не должно меняться"
            assert counters["admin"] == 1, "Число админов не должно меняться"


    @pytest.mark.smoke
    @pytest.mark.stat_counters
    @pytest.mark.not_parallel
    @allure.title("Проверка удаления пользователя и корректное обновление счетчиков статистики после удаления")
    @allure.severity(Severity.CRITICAL)
    def test_statistics_update_after_delete_user(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
            counters_before = logged_in_admin_page.get_current_counters()
        with allure.step(f"Удаляем пользователя {temp_user_name}"):
            logged_in_admin_page.delete_user(temp_user_name)
        with allure.step("Проверяем счетчики статистики пользователей"):
            counters_after = logged_in_admin_page.get_current_counters()
            assert counters_after["total"] == counters_before["total"] - 1, "Общее число пользователей должно стать на 1 меньше"
            assert counters_after["active"] == counters_before["active"] - 1, "Число активных пользователей должно стать на 1 меньше"
            assert counters_after["blocked"] == counters_before["blocked"], "Число заблокированных пользователей не должно меняться"
            assert counters_after["admin"] == counters_before["admin"], "Число админов не должно меняться"


    @allure.title("Проверка отображения пользователей")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "name",
        [
            "Ильшат Насыров",
            "Админ Системы",
            "Демо Юзер",
        ]
    )
    def test_users_list_display_users(self, logged_in_admin_page: AdminPage, name: str):

        with allure.step(f"Проверяем отображение пользователя {name}"):
            logged_in_admin_page.check_user_in_userlist(name)


    @allure.title("Проверка отображения панели редактирования")
    @allure.severity(Severity.NORMAL)
    def test_displaying_edit_panel(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(temp_user_name)
        with allure.step("Закрываем панель редактирования"):
            logged_in_admin_page.edit_panel.close()


    @allure.title("Проверка отображения метки 'Это вы' у админа")
    @allure.severity(Severity.NORMAL)
    def test_current_user_marker(self, logged_in_admin_page: AdminPage):

        with allure.step("Проверяем метку 'Это вы' у админа"):
            logged_in_admin_page.users.check_its_you_label_at_admin_in_users_list()


    @allure.title("Проверка отображения лейблов у админа")
    @allure.severity(Severity.NORMAL)
    def test_admin_labels(self, logged_in_admin_page: AdminPage):

        with allure.step("Проверяем лейблы у админа"):
            logged_in_admin_page.users.check_admin_labels_active_and_admin("Админ Системы")


    @allure.title("Проверка отображения лейблов у пользователя")
    @allure.severity(Severity.NORMAL)
    def test_user_labels(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Проверяем лейблы у пользователя"):
            logged_in_admin_page.users.check_user_labels_active_and_user(temp_user_name)


    @pytest.mark.smoke
    @pytest.mark.admin_search
    @allure.title("Проверка поиска пользователя по имени")
    @allure.severity(Severity.CRITICAL)
    def test_search_by_name(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        target_name = "Ильшат Насыров"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step(f"Выполняем поиск пользователя по имени {target_name}"):
            logged_in_admin_page.fill_search(target_name)
        with allure.step(f"Проверяем, что отображается пользователь с именем {target_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(target_name)
        with allure.step(f"Проверяем, что пользователь с именем {temp_user_name} не отображается"):
            logged_in_admin_page.users.check_not_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Очищаем поиск"):
            logged_in_admin_page.clear_search()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @pytest.mark.smoke
    @pytest.mark.admin_search
    @allure.title("Проверка поиска пользователя по email")
    @allure.severity(Severity.CRITICAL)
    def test_search_by_email(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        target_name = "Ильшат Насыров"
        target_email = "ilshat@example.ru"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step(f"Выполняем поиск пользователя по email {target_email}"):
            logged_in_admin_page.fill_search(target_email)
        with allure.step(f"Проверяем, что отображается пользователь {target_name} с искомым email {target_email}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(target_name)
            logged_in_admin_page.users.check_visible_user_email_in_users_list(target_name, target_email)
        with allure.step(f"Проверяем, что пользователь с именем {temp_user_name} не отображается"):
            logged_in_admin_page.users.check_not_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Очищаем поиск"):
            logged_in_admin_page.clear_search()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @pytest.mark.admin_search
    @allure.title("Проверка поиска несуществующего пользователя")
    @allure.severity(Severity.NORMAL)
    def test_search_no_results(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        target_search = "Несуществующий"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step(f"Выполняем поиск '{target_search}'"):
            logged_in_admin_page.fill_search(target_search)
        with allure.step("Проверяем, что пользователи не найдены"):
            logged_in_admin_page.users.check_visible_users_list_with_not_users()
        with allure.step("Очищаем поиск"):
            logged_in_admin_page.clear_search()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @pytest.mark.admin_search
    @allure.title("Проверка регистронезависимого поиска")
    @allure.severity(Severity.NORMAL)
    def test_search_case_insensitive(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        target_name = "Ильшат Насыров"
        search_case_insensitive = "ИЛЬШАТ НАСЫРОВ"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Выполняем поиск 'ИЛЬШАТ НАСЫРОВ'"):
            logged_in_admin_page.fill_search(search_case_insensitive)
        with allure.step(f"Проверяем, что отображается пользователь с именем {target_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(target_name)
        with allure.step(f"Проверяем, что пользователь с именем {temp_user_name} не отображается"):
            logged_in_admin_page.users.check_not_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Очищаем поиск"):
            logged_in_admin_page.clear_search()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @pytest.mark.admin_search
    @allure.title("Проверка частичного совпадения поиска")
    @allure.severity(Severity.NORMAL)
    def test_search_partial_match(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        target_name = "Ильшат Насыров"
        search_partial_match = "иль"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Выполняем поиск 'иль'"):
            logged_in_admin_page.fill_search(search_partial_match)
        with allure.step(f"Проверяем, что отображается пользователь с именем {target_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(target_name)
        with allure.step(f"Проверяем, что пользователь с именем {temp_user_name} не отображается"):
            logged_in_admin_page.users.check_not_visible_user_in_users_list_with_users(temp_user_name)
        with allure.step("Очищаем поиск"):
            logged_in_admin_page.clear_search()
        with allure.step(f"Проверяем, что отображается пользователь с именем {temp_user_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @allure.title("Проверка отсутствия возможности у Админа удалить самого себя")
    @allure.severity(Severity.NORMAL)
    def test_cannot_delete_self(self, logged_in_admin_page: AdminPage):

        with allure.step("Проверяем, что Админ не может удалить сам себя"):
            logged_in_admin_page.delete_admin()


    @pytest.mark.smoke
    @allure.title("Проверка смены роли пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_edit_user_role(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(temp_user_name)
        with allure.step("Меняем роль 'Пользователь' на 'Админ'"):
            logged_in_admin_page.change_role_to_admin()
        with allure.step("Проверяем, что метка у пользователя стала 'Админ'"):
            logged_in_admin_page.users.check_admin_labels_active_and_admin(temp_user_name)


    @pytest.mark.smoke
    @allure.title("Проверка редактирования имени пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_edit_user_name(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        new_name = "Update_name"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(temp_user_name)
        with allure.step("Редактируем имя сотрудника"):
            logged_in_admin_page.name_editing(new_name)
        with allure.step(f"Проверяем, что имя у пользователя в списке поменялось на {new_name}"):
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(new_name)
        with allure.step("Меняем имя сотрудника на прежнее"):
            logged_in_admin_page.open_user_edit_panel(new_name)
            logged_in_admin_page.name_editing(temp_user_name)
            logged_in_admin_page.users.check_visible_user_in_users_list_with_users(temp_user_name)


    @pytest.mark.smoke
    @allure.title("Проверка смены пароля пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_edit_user_password(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        user_name = user_unauthenticated["name"]
        user_email = user_unauthenticated["email"]
        new_user_password = "Update_password"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(user_name)
        with allure.step("Меняем пароль сотрудника"):
            logged_in_admin_page.password_editing(new_user_password)
        with allure.step("Разлогиниваемся и проверяем, что отображается окно авторизации"):
            logged_in_admin_page.click_logout_button()
            logged_in_admin_page.login.check_visible()
        with allure.step(f"Авторизуемся под пользователем {user_name} с новым паролем"):
            logged_in_admin_page.login.fill_login_form(user_email, new_user_password)
            logged_in_admin_page.login.click_login_button()
        with allure.step("Проверяем, что пользователь успешно авторизован"):
            logged_in_admin_page.navbar.check_visible_username(user_name)
            logged_in_admin_page.tasks.check_visible_with_no_tasks()


    @pytest.mark.smoke
    @allure.title("Проверка редактирования email пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_edit_user_email(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        unique_id = uuid.uuid4().hex[:6]
        new_email = f"update_{unique_id}@example.com"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(temp_user_name)
        with allure.step("Редактируем email сотрудника"):
            logged_in_admin_page.email_editing(new_email)
        with allure.step(f"Проверяем, что email у пользователя в списке поменялся на {new_email}"):
            logged_in_admin_page.users.check_visible_user_email_in_users_list(temp_user_name, new_email)
        with allure.step(f"Удаляем пользователя {temp_user_name}"):
            logged_in_admin_page.delete_user(temp_user_name)


    @allure.title("Проверка вывода ошибки об использовании занятого email при редактировании пользователя")
    @allure.severity(Severity.NORMAL)
    def test_choice_used_email(self, user_unauthenticated: dict, logged_in_admin_page: AdminPage):

        temp_user_name = user_unauthenticated["name"]
        new_email = "admin@example.com"

        with allure.step("Обновляем данные на странице"):
            logged_in_admin_page.reload()
        with allure.step("Открываем панель редактирования сотрудника"):
            logged_in_admin_page.open_user_edit_panel(temp_user_name)
        with allure.step("Вводим занятый email и проверяем, что появилось окно с ошибкой - email уже занят"):
            logged_in_admin_page.entering_used_email(new_email)
        with allure.step("Проверяем, что форма редактирования не закрылась"):
            logged_in_admin_page.edit_panel.check_visible()
        with allure.step("Закрываем форму редактирования по крестику"):
            logged_in_admin_page.edit_panel.close()


    @allure.title("Проверка перехода на страницу дашборда")
    @allure.severity(Severity.NORMAL)
    def test_navigation_to_dashboard(self, logged_in_admin_page: AdminPage):

        with allure.step("Переходим на страницу дашборда и проверяем, что отображается пустой список задач"):
            logged_in_admin_page.click_to_dashboard_link()


    @allure.title("Проверка выхода из приложения")
    @allure.severity(Severity.NORMAL)
    def test_navigation_to_logout(self, logged_in_admin_page: AdminPage):

        with allure.step("Разлогиниваемся и проверяем, что отображается окно авторизации"):
            logged_in_admin_page.click_logout_button()
            logged_in_admin_page.login.check_visible()

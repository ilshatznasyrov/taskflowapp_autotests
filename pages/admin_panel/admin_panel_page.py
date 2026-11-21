import allure

from pages.admin_panel.edit_panel_page import EditPanelPage
from pages.authentication.login_page import LoginPage
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from components.users_list.users_list_component import UsersListComponent
from components.task_list.task_list_component import TaskListComponent
from components.navigation.navbar_component import NavbarComponent


class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.logo_text = page.locator(".logo")
        self.to_dashboard_link = page.get_by_test_id("to-dashboard")
        self.logout_button = page.get_by_test_id("logout-button")
        self.stat_total_users = page.get_by_test_id("stat-total-users")
        self.stat_active_users = page.get_by_test_id("stat-active-users")
        self.stat_blocked_users = page.get_by_test_id("stat-blocked-users")
        self.stat_admin_users = page.get_by_test_id("stat-admin-users")
        self.search_users = page.get_by_test_id("search-users")
        self.users_list = page.get_by_test_id("users-list")

        self.users = UsersListComponent(page)
        self.tasks = TaskListComponent(page)
        self.navbar = NavbarComponent(page)
        self.edit_panel = EditPanelPage(page)
        self.login = LoginPage(page)


    def check_visible(self):

        expect(self.logo_text).to_be_visible()
        expect(self.to_dashboard_link).to_be_visible()
        expect(self.stat_total_users).to_be_visible()
        expect(self.stat_active_users).to_be_visible()
        expect(self.stat_blocked_users).to_be_visible()
        expect(self.stat_admin_users).to_be_visible()
        expect(self.search_users).to_be_visible()
        expect(self.users_list).to_be_visible()


    @allure.step("Проверяем текущие значения счетчиков статистики")
    def get_current_counters(self) -> dict[str, int]:
        """
        Возвращает текущие значения счетчиков в виде целых чисел.
        """

        return {
            "total": int(self.stat_total_users.text_content().strip()),
            "active": int(self.stat_active_users.text_content().strip()),
            "blocked": int(self.stat_blocked_users.text_content().strip()),
            "admin": int(self.stat_admin_users.text_content().strip()),
        }


    def check_user_in_userlist(self, username: str):

        self.users.check_visible_user_in_users_list_with_users(username)


    def check_counters(self, total: str, active: str, blocked: str, admin: str):

        expect(self.stat_total_users).to_be_visible()
        expect(self.stat_total_users).to_have_text(total)

        expect(self.stat_active_users).to_be_visible()
        expect(self.stat_active_users).to_have_text(active)

        expect(self.stat_blocked_users).to_be_visible()
        expect(self.stat_blocked_users).to_have_text(blocked)

        expect(self.stat_admin_users).to_be_visible()
        expect(self.stat_admin_users).to_have_text(admin)


    def check_search(self):

        expect(self.search_users).to_be_visible()


    def fill_search(self, target_search: str):

        self.search_users.fill(target_search)


    def clear_search(self):

        self.search_users.clear()


    def blocking_user(self, username: str):

        self.users.blocking_user_in_users_list(username)


    def unblocking_user(self, username: str):

        self.users.unblocking_user_in_users_list(username)


    def delete_user(self, username: str):

        self.users.delete_user_in_users_list(username)


    def delete_admin(self):

        self.users.check_not_delete_btn_at_admin_in_users_list()


    @allure.step("Кликаем на пункт 'К задачам' в навбаре")
    def click_to_dashboard_link(self):

        self.to_dashboard_link.click()
        self.tasks.check_visible_with_no_tasks()


    def click_logout_button(self):

        self.navbar.check_visible_logout_button()
        self.navbar.click_logout()


    def open_user_edit_panel(self, username: str):

        self.users.open_edit_panel(username)
        self.edit_panel.check_visible()


    def change_role_to_admin(self):

        self.edit_panel.change_role("Администратор")


    def name_editing(self, username: str):

        self.edit_panel.change_name(username)


    def password_editing(self, password: str):

        self.edit_panel.change_password(password)


    def email_editing(self, email: str):

        self.edit_panel.change_email(email)


    def entering_used_email(self, email: str):

        self.edit_panel.check_error_save_editing(email)

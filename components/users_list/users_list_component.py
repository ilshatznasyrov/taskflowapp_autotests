import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent
from components.user_item.user_item_component import UserItemComponent


class UsersListComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.users_list = page.get_by_test_id("users-list")
        self.admin_name = "Админ Системы"


    def check_visible_user_in_users_list_with_users(self, username: str):

        expect(self.users_list).to_be_visible()

        user = UserItemComponent(self.page, username)
        user.check_visible()
        user.check_name(username)


    def check_not_visible_user_in_users_list_with_users(self, username: str):

        expect(self.users_list).to_be_visible()

        user = UserItemComponent(self.page, username)
        user.check_not_visible()


    def check_visible_users_list_with_not_users(self):

        expect(self.users_list).to_be_visible()
        expect(self.users_list).to_contain_text("Пользователи не найдены")


    def check_visible_user_email_in_users_list(self, username: str, email: str):

        user = UserItemComponent(self.page, username)
        user.check_email(email)


    def blocking_user_in_users_list(self, username: str):

        user = UserItemComponent(self.page, username)
        user.blocking_user()
        user.check_status_blocked()


    def unblocking_user_in_users_list(self, username: str):

        user = UserItemComponent(self.page, username)
        user.unblocking_user()
        user.check_status_unblocked()


    def delete_user_in_users_list(self, username: str):

        user = UserItemComponent(self.page, username)
        user.delete_user()
        user.check_not_visible()


    @allure.step("Проверяем, что нет кнопки удаления Админа в списке сотрудников")
    def check_not_delete_btn_at_admin_in_users_list(self):

        user = UserItemComponent(self.page, self.admin_name)
        user.check_not_visible_delete_btn()


    def check_its_you_label_at_admin_in_users_list(self):

        user = UserItemComponent(self.page, self.admin_name)
        user.check_its_you_label()


    @allure.step("Проверяем, что отображаются лейблы 'Активен' и 'Пользователь'")
    def check_user_labels_active_and_user(self, username: str):

        user = UserItemComponent(self.page, username)

        expect(user.badge_active).to_be_visible()
        expect(user.badge_active).to_have_text("Активен")

        expect(user.badge_user).to_be_visible()
        expect(user.badge_user).to_have_text("Пользователь")


    @allure.step("Проверяем, что отображаются лейблы 'Активен' и 'Админ'")
    def check_admin_labels_active_and_admin(self, username: str):

        admin = UserItemComponent(self.page, username)

        expect(admin.badge_active).to_be_visible()
        expect(admin.badge_active).to_have_text("Активен")

        expect(admin.badge_admin).to_be_visible()
        expect(admin.badge_admin).to_have_text("Админ")


    def open_edit_panel(self, username: str):

        user = UserItemComponent(self.page, username)
        user.click_edit_btn()


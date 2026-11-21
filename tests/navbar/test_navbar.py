import pytest
import allure
from allure_commons.types import Severity
from pages.dashboard.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.navbar
@allure.tag("web")
@allure.feature("Навигационная панель")
class TestNavbar:

    @allure.title("Проверка отображения названия приложения")
    @allure.severity(Severity.NORMAL)
    def test_app_title_display(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что  название приложения отображается в навбаре"):
            dashboard_page.navbar.check_visible_logo()


    @pytest.mark.smoke
    @allure.title("Проверка отображения имени пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_username_display(self, dashboard_page: DashboardPage, user_authenticated: dict):

        user_name = user_authenticated["name"]

        with allure.step("Проверяем, что  имя пользователя отображается в навбаре"):
            dashboard_page.navbar.check_visible_username(user_name)


    @pytest.mark.smoke
    @allure.title("Проверка выхода из аккаунта")
    @allure.severity(Severity.CRITICAL)
    def test_user_logout(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Проверяем, что кнопка выхода из аккаунта отображается в навбаре"):
            dashboard_page.navbar.check_visible_logout_button()
        with allure.step("Выходим из аккаунта и проверяем, что выход выполнился успешно"):
            dashboard_page.navbar.click_logout()


    @allure.title("Проверка клика на название приложения")
    @allure.severity(Severity.NORMAL)
    def test_click_app_title(self, dashboard_page: DashboardPage, user_authenticated: dict):

        with allure.step("Кликаем на лого в навбаре"):
            dashboard_page.navbar.click_logo()
        with allure.step("Проверяем, что остались на странице дашборда"):
            dashboard_page.check_toolbar()
            dashboard_page.navbar.check_visible_logo()
            dashboard_page.navbar.check_visible_logout_button()

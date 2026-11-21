import allure
import pytest
from allure_commons.types import Severity
from pages.authentication.login_page import LoginPage
from config import settings


@pytest.mark.regression
@pytest.mark.authorization
@allure.tag("web")
@allure.feature("Авторизация")
class TestAuthorization:


    @pytest.mark.smoke
    @allure.title("Проверка успешной авторизации пользователя с ролью 'Пользователь'")
    @allure.severity(Severity.BLOCKER)
    def test_successful_authorization_with_role_user(self, login_page: LoginPage):

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step(f"Авторизуемся с корректным логином и паролем под пользователем с ролью 'Пользователь'"):
            login_page.fill_login_form(
                email=settings.demo_email,
                password=settings.demo_password.get_secret_value()
            )
            login_page.click_login_button()
        with allure.step("Проверяем, что успешно авторизовались"):
            login_page.check_successful_login_with_role_user()


    @pytest.mark.smoke
    @allure.title("Проверка успешной авторизации пользователя с ролью 'Администратор'")
    @allure.severity(Severity.BLOCKER)
    def test_successful_authorization_with_role_admin(self, login_page: LoginPage):

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step(f"Авторизуемся с корректным логином и паролем под пользователем с ролью 'Администратор'"):
            login_page.fill_login_form(
                email=settings.admin_email,
                password=settings.admin_password.get_secret_value()
            )
            login_page.click_login_button()
        with allure.step("Проверяем, что успешно авторизовались"):
            login_page.check_successful_login_with_role_admin()


    @pytest.mark.smoke
    @allure.title("Проверка перехода на страницу регистрации")
    @allure.severity(Severity.CRITICAL)
    def test_open_registration_page(self, login_page: LoginPage):
        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Переходим на страницу регистрации"):
            login_page.click_register_link()
        with allure.step("Проверяем, что открылась форма регистрации"):
            login_page.check_go_to_registration_page()


    @pytest.mark.smoke
    @allure.title("Проверка авторизации заблокированного пользователя")
    @allure.severity(Severity.CRITICAL)
    def test_authorization_with_blocked_user(self, login_page: LoginPage):

        error_message_text = "Ваш аккаунт заблокирован. Обратитесь к администратору."

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Авторизуемся под заблокированным пользователем"):
            login_page.fill_login_form(
                email=settings.user_email,
                password=settings.user_password.get_secret_value()
            )
            login_page.click_login_button()
        with allure.step("Проверяем, что отображается сообщение 'Ваш аккаунт заблокирован' и авторизация не выполнилась"):
            login_page.check_visible_error_message(error_message_text)
            login_page.check_visible_login_button()


    @pytest.mark.smoke
    @allure.title("Проверка авторизации с некорректным паролем")
    @allure.severity(Severity.CRITICAL)
    def test_incorrect_password_authorization(self, login_page: LoginPage):

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Авторизуемся с некорректным паролем"):
            login_page.fill_login_form(email="ilshat@example.com", password="123")
            login_page.click_login_button()
        with allure.step("Проверяем отображение ошибки валидации для некорректного пароля"):
            login_page.check_password_validation_error()
        with allure.step("Проверяем, что кнопка входа осталась доступна"):
            login_page.check_visible_login_button()


    @allure.title("Проверка авторизации с неверным логином или паролем")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "email, password",
        [
            ("ilshat@example.com", "ilshat123"),
            ("ilshat@example.ru", "ilshat")
        ]
    )
    def test_wrong_email_or_password_authorization(self, login_page: LoginPage, email: str, password: str):

        error_message_text = "Неверный email или пароль"

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Авторизуемся с неверным логином / паролем"):
            login_page.fill_login_form(email=email, password=password)
            login_page.click_login_button()
        with allure.step("Проверяем, что отображается сообщение 'Неверный email или пароль' и авторизация не выполнилась"):
            login_page.check_visible_error_message(error_message_text)
            login_page.check_visible_login_button()


    @allure.title("Проверка авторизации с пустым логином или паролем")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "email, password",
        [
            ("ilshat@example.com", ""),
            ("", "ilshat")
        ]
    )
    def test_empty_email_or_password_authorization(self, login_page: LoginPage, email: str, password: str):

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Авторизуемся с пустым логином / паролем"):
            login_page.fill_login_form(email=email, password=password)
            login_page.click_login_button()
        with allure.step("Проверяем, что кнопка входа осталась доступна и авторизация не выполнилась"):
            login_page.check_visible_login_button()


    @pytest.mark.skip("Вывод ошибки валидации для некорректного email пока не реализован в проекте (для демонстрации skip теста)")
    @allure.title("Проверка авторизации с некорректным email")
    @allure.severity(Severity.NORMAL)
    def test_incorrect_email_authorization(self, login_page: LoginPage):

        with allure.step("Открываем сайт на странице авторизации"):
            login_page.open_login_page()
        with allure.step("Авторизуемся с некорректным email"):
            login_page.fill_login_form(email="ilshatexample.com", password="ilshat")
            login_page.click_login_button()
        with allure.step("Проверяем отображение ошибки валидации для некорректного email"):
            login_page.check_email_validation_error()
        with allure.step("Проверяем, что кнопка входа осталась доступна"):
            login_page.check_visible_login_button()

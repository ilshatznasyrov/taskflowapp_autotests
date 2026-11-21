import uuid
import allure
import pytest
from allure_commons.types import Severity
from pages.authentication.login_page import LoginPage
from pages.authentication.registration_page import RegistrationPage
from tools.supabase_utils import delete_user_by_email


@pytest.mark.regression
@pytest.mark.registration
@allure.tag("web")
@allure.feature("Регистрация")
class TestRegistration:


    @pytest.mark.smoke
    @allure.title("Проверка успешной регистрации")
    @allure.severity(Severity.BLOCKER)
    def test_successful_registration(self, user_authenticated: dict, registration_page: RegistrationPage):

        user_name = user_authenticated["name"]

        with allure.step("Проверяем, что сообщение об успехе отображается и ошибок нет"):
            registration_page.check_visible_success_message()
            registration_page.check_not_visible_error_message()
        with allure.step("Проверяем, что открылась страница дашборда"):
            registration_page.check_open_dashboard_page()
        with allure.step(f"Проверяем, что в навбаре отображается имя пользователя {user_name}"):
            registration_page.dashboard_page.navbar.check_visible_username(user_name)
        with allure.step("Проверяем, что у нового пользователя пустой список задач"):
            registration_page.dashboard_page.check_tasks_list_with_no_tasks()


    @allure.title("Проверка успешной регистрации с нестандартными символами в имени пользователя")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.parametrize(
        "name",
        [
            "123",
            "№()@#$%&-+!",
            "NORM",
        ]
    )
    def test_registration_with_special_characters_in_name(self,
                                                          registration_page: RegistrationPage,
                                                          user_data,
                                                          name: str,
                                                          request):
        """
        Проверяется успешная регистрация с граничными значениями в имени
        (только цифры, спецсимволы, верхний регистр).

        Архитектурное примечание:
        - Уникальный email генерируется внутри теста для каждой итерации параметризации.
        - Очистка выполняется через request.addfinalizer + Supabase API. Это гарантирует,
          что будет удалена именно та запись, которая создана в текущей итерации,
          даже если тест упадет на этапе проверок.
        """

        unique_email = f"test_{uuid.uuid4().hex[:4]}@example.com"

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step(f"Заполняем форму регистрации с именем '{name}' и уникальным email"):
            registration_page.fill_register_form(username=name, email=unique_email,
                                                     password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что успешно зарегистрировались"):
            registration_page.check_visible_success_message()
            registration_page.check_not_visible_error_message()
            registration_page.check_open_dashboard_page()
        with allure.step(f"Проверяем, что в навбаре отображается имя пользователя {name}"):
            registration_page.dashboard_page.navbar.check_visible_username(name)
        with allure.step("Проверяем, что у нового пользователя пустой список задач"):
            registration_page.dashboard_page.check_tasks_list_with_no_tasks()

        # --------------- teardown ---------------
        def cleanup_user():
            """Функция для удаления тестовых пользователей, выполнится после завершения теста"""
            try:
                deleted_count = delete_user_by_email(unique_email)
                if deleted_count > 0:
                    print(f"\nПользователь успешно удален: {unique_email}")
                else:
                    print(f"\nПользователь {unique_email} уже был удален. Очистка не требуется.")

            except Exception as e:
                # не роняем тест, если очистка не сработала, просто логируем
                print(f"\nОшибка удаления {unique_email}: {e}")

        request.addfinalizer(cleanup_user)


    @pytest.mark.smoke
    @allure.title("Проверка выхода из формы регистрации на страницу авторизации")
    @allure.severity(Severity.CRITICAL)
    def test_open_login_page(self, registration_page: RegistrationPage, login_page: LoginPage):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Выходим из формы регистрации на страницу авторизации"):
            registration_page.click_login_link()
        with allure.step("Проверяем, что открылась страница авторизации"):
            login_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при вводе занятого email")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_email_occupied(self, registration_page: RegistrationPage, user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с занятым email"):
            # Используем email из ранее созданного аккаунта
            registration_page.fill_register_form(username=user_data["name"], email="demo@example.com",
                                                 password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что появилось сообщение 'Пользователь с таким email уже существует' и регистрация не выполнилась"):
            registration_page.check_visible_error_message()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при вводе некорректного email")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_incorrect_email(self, registration_page: RegistrationPage, user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с некорректным email"):
            registration_page.fill_register_form(username=user_data["name"], email="pumpkinexample@com",
                                                 password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что появилось сообщение 'Введите корректный email' и регистрация не выполнилась"):
            registration_page.check_email_error_message()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при вводе имени пользователя менее 2 символов")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_short_name(self, registration_page: RegistrationPage, user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с именем длиной менее 2 символов"):
            registration_page.fill_register_form(username="a", email=user_data["email"],
                                                 password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что появилось сообщение 'Имя должно содержать не менее 2 символов' и регистрация не выполнилась"):
            registration_page.check_name_error_message()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации c пустым именем")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_empty_name(self, registration_page: RegistrationPage,
                                                           user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с пустым именем"):
            registration_page.fill_register_form(username="", email=user_data["email"], password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что остались в форме регистрации и регистрация не выполнилась"):
            registration_page.check_empty_name_field_validation()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при вводе пробела в email")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_space_in_email(self, registration_page: RegistrationPage,
                                                           user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с пробелом в email"):
            registration_page.fill_register_form(username=user_data["name"], email="email @example.com", password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что остались в форме регистрации и регистрация не выполнилась"):
            registration_page.check_empty_email_field_validation()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации с пустым email")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_empty_email(self, registration_page: RegistrationPage,
                                                        user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с пустым email"):
            registration_page.fill_register_form(username=user_data["name"], email="", password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что остались в форме регистрации и регистрация не выполнилась"):
            registration_page.check_empty_email_field_validation()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при несовпадении пароля и его подтверждения")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_incorrect_confirm_password(self, registration_page: RegistrationPage, user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с несовпадением пароля и его подтверждения"):
            registration_page.fill_register_form_with_incorrect_confirm_password(username=user_data["name"], email=user_data["email"],
                                                 password=user_data["password"])
            registration_page.click_register_button()
        with allure.step("Проверяем, что появилось сообщение 'Пароли не совпадают' и регистрация не выполнилась"):
            registration_page.check_confirm_password_error_message()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при вводе пароля менее 6 символов")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_short_password(self, registration_page: RegistrationPage,
                                                                       user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с паролем длиной менее 6 символов"):
            registration_page.fill_register_form(username=user_data["name"], email=user_data["email"], password="12345")
            registration_page.click_register_button()
        with allure.step("Проверяем, что появилось сообщение 'Пароль должен быть не менее 6 символов' и регистрация не выполнилась"):
            registration_page.check_password_error_message()
            registration_page.check_visible()


    @allure.title("Проверка валидация формы регистрации при пустом пароле")
    @allure.severity(Severity.NORMAL)
    def test_unsuccessful_registration_with_empty_password(self, registration_page: RegistrationPage,
                                                           user_data):

        with allure.step("Открываем сайт на странице регистрации"):
            registration_page.open_registration_page()
        with allure.step("Заполняем форму регистрации с пустым паролем"):
            registration_page.fill_register_form(username=user_data["name"], email=user_data["email"], password="")
            registration_page.click_register_button()
        with allure.step("Проверяем, что остались в форме регистрации и регистрация не выполнилась"):
            registration_page.check_empty_password_field_validation()
            registration_page.check_visible()

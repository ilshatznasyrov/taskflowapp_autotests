import re
import uuid
import pytest
from dotenv import load_dotenv
from typing import Iterator
from playwright.sync_api import Page, Playwright, expect
from config import settings
from _pytest.fixtures import SubRequest

from tools.pages import initialize_playwright_page

from pages.authentication.login_page import LoginPage
from pages.authentication.registration_page import RegistrationPage
from pages.admin_panel.admin_panel_page import AdminPage
from tools.supabase_utils import delete_user_by_email

load_dotenv()  # читает файл .env


@pytest.fixture(params=settings.browsers)
def page(request: SubRequest, playwright: Playwright) -> Iterator[Page]:

    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name,
        browser_type=request.param
    )


@pytest.fixture(scope="session")
def authenticated_state(playwright: Playwright, user_data) -> None:
    """
    Фикстура регистрирует пользователя один раз за сессию и сохраняет состояние браузера.
    """

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{settings.app_url}/register.html", wait_until="networkidle")

    name_input = page.get_by_test_id("name-input")
    email_input = page.get_by_test_id("email-input")
    password_input = page.get_by_test_id("password-input")
    confirm_password_input = page.get_by_test_id("confirm-password-input")
    register_button = page.get_by_test_id("register-button")

    name_input.fill(user_data["name"])
    email_input.fill(user_data["email"])
    password_input.fill(user_data["password"])
    confirm_password_input.fill(user_data["password"])
    register_button.click()

    page.wait_for_url("**/dashboard.html")

    # сохраняем состояние (куки, localStorage) в файл
    context.storage_state(path=settings.browser_state_file)

    browser.close()


@pytest.fixture(params=settings.browsers)
def page_with_state(request: SubRequest, authenticated_state, playwright: Playwright) -> Iterator[Page]:

    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name,
        browser_type=request.param,
        storage_state=settings.browser_state_file
    )


@pytest.fixture
def logged_in_admin_page(login_page: LoginPage) -> AdminPage:
    """
    Фикстура выполняет вход под админом и возвращает объект AdminPage.
    """

    target_page = login_page.page

    target_page.goto(f"{settings.app_url}/index.html", wait_until="domcontentloaded")

    login_page.fill_login_form(
        email=settings.admin_email,
        password=settings.admin_password.get_secret_value()
    )
    login_page.click_login_button()
    expect(target_page).to_have_url(re.compile(r".*(admin|dashboard)\.html/?$"), timeout=10000)

    return AdminPage(target_page)


@pytest.fixture
def user_unauthenticated(page: Page, registration_page: RegistrationPage):
    """
    Фикстура создает пользователя через UI и очищает сессию.
    Используется в тестах админки.
    """

    unique_id = uuid.uuid4().hex[:6]
    temp_name = f"TestUser_{unique_id}"
    temp_email = f"test_{unique_id}@example.com"
    temp_password = "Test123!"

    registration_page.visit(f"{settings.app_url}/register.html")
    registration_page.fill_register_form(
        username=temp_name, email=temp_email, password=temp_password
    )
    registration_page.click_register_button()

    page.wait_for_url("**/dashboard.html", timeout=15000)

    # очищаем сессию, чтобы следующая фикстура могла залогинить админа
    page.context.clear_cookies()
    page.evaluate("() => localStorage.clear()")

    yield {
        "name": temp_name,
        "email": temp_email,
        "password": temp_password
    }

    try:
        deleted_count = delete_user_by_email(temp_email)
        if deleted_count > 0:
            print(f"\nПользователь успешно удален: {temp_email}")
        else:
            print(f"\nПользователь {temp_email} уже был удален")

    except Exception as e:
        print(f"\nОшибка удаления: {e}")


@pytest.fixture
def user_authenticated(page: Page, registration_page: RegistrationPage):
    """
    Фикстура создает пользователя через UI и не очищает сессию браузера.
    После теста удаляет пользователя через Supabase API.
    """

    unique_id = uuid.uuid4().hex[:6]
    temp_name = f"TestUser_{unique_id}"
    temp_email = f"test_{unique_id}@example.com"
    temp_password = "Test123!"

    registration_page.visit(f"{settings.app_url}/register.html")
    registration_page.fill_register_form(username=temp_name, email=temp_email, password=temp_password)
    registration_page.click_register_button()

    page.wait_for_load_state("networkidle")

    yield {
        "name": temp_name,
        "email": temp_email,
        "password": temp_password
    }

    try:
        deleted_count = delete_user_by_email(temp_email)
        if deleted_count > 0:
            print(f"\nПользователь успешно удален: {temp_email}")
        else:
            print(f"\nПользователь {temp_email} уже был удален")

    except Exception as e:
        print(f"\nОшибка удаления: {e}")

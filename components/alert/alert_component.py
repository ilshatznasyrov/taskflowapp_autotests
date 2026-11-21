import allure
from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class AlertComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.alert_container = page.locator("#alertModal")
        self.alert_message = page.locator("//div[@class=\"alert-message\"]")
        self.alert_button = page.locator("//button[@class=\"alert-btn\"]")
        self.confirm_container = page.locator("#confirmIcon")
        self.confirm_message = page.locator("#confirmMessage")
        self.confirm_button_ok = page.locator("#confirmOk")
        self.confirm_button_cancel = page.locator("#confirmCancel")


    @allure.step("Проверяем, что окно с сообщением об успешном создании задачи появилось")
    def check_visible_alert_of_creation(self):

        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Задача успешно создана")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением об успешном обновлении задачи появилось")
    def check_visible_alert_of_update(self):

        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Задача успешно обновлена")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением об успешном удалении задачи появилось")
    def check_visible_alert_of_delete(self):
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Задача успешно удалена")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением о блокировке пользователя появилось")
    def check_visible_alert_block_user(self):

        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Пользователь заблокировать")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением о разблокировке пользователя появилось")
    def check_visible_alert_unblock_user(self):

        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Пользователь разблокировать")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением об удалении пользователя появилось")
    def check_visible_alert_delete_user(self):

        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Пользователь удалён")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением 'Введите заголовок задачи' появилось")
    def check_visible_alert_not_title(self):
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Введите заголовок задачи")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением 'Пользователь успешно обновлён' появилось")
    def check_visible_alert_user_update(self):
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Пользователь успешно обновлён")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно с сообщением 'Ошибка при сохранении' появилось")
    def check_visible_alert_error_save_editing(self):
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_contain_text("Ошибка при сохранении")
        expect(self.alert_button).to_be_visible()
        expect(self.alert_button).to_have_text("OK")


    @allure.step("Проверяем, что окно подтверждения удаления задачи появилось")
    def check_visible_confirm_of_delete(self):

        expect(self.confirm_message).to_be_visible()
        expect(self.confirm_message).to_have_text("Удалить задачу?")
        expect(self.confirm_button_cancel).to_be_visible()
        expect(self.confirm_button_cancel).to_have_text("Отмена")
        expect(self.confirm_button_ok).to_be_visible()
        expect(self.confirm_button_ok).to_have_text("OK")


    @allure.step("Проверяем, что окно подтверждения блокировки пользователя появилось")
    def check_visible_confirm_of_block_user(self):

        expect(self.confirm_message).to_be_visible()
        expect(self.confirm_message).to_contain_text("Заблокировать пользователя")
        expect(self.confirm_button_cancel).to_be_visible()
        expect(self.confirm_button_cancel).to_have_text("Отмена")
        expect(self.confirm_button_ok).to_be_visible()
        expect(self.confirm_button_ok).to_have_text("OK")


    @allure.step("Проверяем, что окно подтверждения разблокировки пользователя появилось")
    def check_visible_confirm_of_unblock_user(self):

        expect(self.confirm_message).to_be_visible()
        expect(self.confirm_message).to_contain_text("Разблокировать пользователя")
        expect(self.confirm_button_cancel).to_be_visible()
        expect(self.confirm_button_cancel).to_have_text("Отмена")
        expect(self.confirm_button_ok).to_be_visible()
        expect(self.confirm_button_ok).to_have_text("OK")


    @allure.step("Проверяем, что окно подтверждения удаления пользователя появилось")
    def check_visible_confirm_of_delete_user(self):

        expect(self.confirm_message).to_be_visible()
        expect(self.confirm_message).to_contain_text("Удалить пользователя")
        expect(self.confirm_button_cancel).to_be_visible()
        expect(self.confirm_button_cancel).to_have_text("Отмена")
        expect(self.confirm_button_ok).to_be_visible()
        expect(self.confirm_button_ok).to_have_text("OK")


    @allure.step("Закрываем окно с сообщением по клику на кнопку 'ОК'")
    def click_alert_button(self):

        self.alert_button.click()


    @allure.step("Подтверждаем действие по клику на кнопку 'ОК'")
    def click_confirm_button_ok(self):

        self.confirm_button_ok.click()


    @allure.step("Отменяем действие по клику на кнопку 'Отмена'")
    def click_confirm_button_cancel(self):

        self.confirm_button_cancel.click()


    @allure.step("Проверяем, что окно с сообщением закрылось")
    def check_alert_closed(self):

        expect(self.alert_container).not_to_be_visible()


    @allure.step("Проверяем, что окно подтверждения закрылось")
    def check_confirm_closed(self):

        expect(self.confirm_container).not_to_be_visible()

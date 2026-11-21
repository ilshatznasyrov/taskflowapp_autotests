# taskflowapp_autotests

Фреймворк UI-автотестов для системы управления задачами **TaskFlow**.  
Написан на стеке: **Python + Playwright + Allure**.

**Демо приложения:** [ilshatznasyrov.github.io/taskflow-app](https://ilshatznasyrov.github.io/taskflow-app)  
**Демо-доступ:** `demo@example.com` / `Demo123!`


---

## Возможности

- **Page Object Model** - чистая архитектура с разделением на Pages и Components
- **Параллельный запуск** - ускорение прогона в 3-5 раз через `pytest-xdist`
- **Allure-отчёты** - детальные HTML-отчёты с видео, скриншотами и трейсами
- **Типизированная конфигурация** - Pydantic Settings с защитой секретов (`SecretStr`)
- **API-очистка данных** - мгновенное удаление тестовых данных через Supabase API
- **Кросс-браузерное тестирование** - Chromium, WebKit, Firefox

---

## Структура тестов

- admin_panel/ - Тесты админ-панели
- authentication/ - Регистрация и авторизация
- dashboard/ - Дашборд, список задач, тулбар
- navbar/ - Навигационная панель
- task_form/ - Создание и редактирование задач

---

## Стек технологий

- **Python 3.13+** 
- **Pytest 9.1** 
- **Playwright 0.9** 
- **Allure 2.16** 
- **Pydantic 2.14** 
- **Supabase SDK** 
- **pytest-xdist** 

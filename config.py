from pathlib import Path
from enum import Enum
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"


class TestUser(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr


class TestData(BaseModel):

    image_png_file: Path | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore"
    )

    # основные настройки
    app_url: HttpUrl
    headless: bool
    browsers: list[Browser]

    supabase_url: HttpUrl
    supabase_service_key: SecretStr
    admin_email: EmailStr
    admin_password: SecretStr
    demo_email: EmailStr
    demo_password: SecretStr
    user_email: EmailStr
    user_password: SecretStr

    # вложенные модели
    test_user: TestUser
    test_data: TestData | None = None

    # пути
    videos_dir: Path = Path("videos")
    tracing_dir: Path = Path("tracing")
    allure_results_dir: Path = Path("allure-results")
    browser_state_file: Path = Path("browser-state.json")

    def setup_directories(self) -> None:
        """Создает необходимые директории и файлы после чтения конфига"""
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.tracing_dir.mkdir(parents=True, exist_ok=True)
        self.allure_results_dir.mkdir(parents=True, exist_ok=True)
        self.browser_state_file.parent.mkdir(parents=True, exist_ok=True)
        self.browser_state_file.touch(exist_ok=True)


# инициализация
settings = Settings()
settings.setup_directories()

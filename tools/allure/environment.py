from config import settings


# Ключи, которые никогда не должны попадать в Environment,
SECRET_FIELD_NAMES = {
    "password",
    "api_key",
    "service_key",
    "secret",
    "token",
}

ALLOWED_ENVIRONMENT_KEYS = {
    "app_url",
    "headless",
    "browsers",
    "admin_email",
    "demo_email",
    "user_email",
    "test_user",
    "videos_dir",
    "tracing_dir",
    "allure_results_dir",
    "browser_state_file",
}

MASKED_KEYS = {
    "supabase_url",
}


def _serialize_value(value) -> str:
    if isinstance(value, list):
        return ", ".join(getattr(item, "value", str(item)) for item in value)

    if isinstance(value, dict):
        # фильтруем вложенные секретные поля перед выводом
        safe_items = {
            k: v for k, v in value.items()
            if k.lower() not in SECRET_FIELD_NAMES
        }
        return ", ".join(f"{k}={v}" for k, v in safe_items.items())

    return str(value)


def create_allure_environment_file():
    data = settings.model_dump(mode="json")

    lines = []
    for key, value in data.items():
        if key in ALLOWED_ENVIRONMENT_KEYS:
            lines.append(f"{key}={_serialize_value(value)}")
        elif key in MASKED_KEYS:
            lines.append(f"{key}=***")

    env_path = settings.allure_results_dir / "environment.properties"
    env_path.write_text("\n".join(lines), encoding="utf-8")

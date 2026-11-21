from supabase import create_client, Client
from config import settings


def delete_user_by_email(email: str) -> int:
    """
    Удаляет пользователя из Supabase по email.
    Возвращает количество удалённых строк.
    """
    client: Client = create_client(
                str(settings.supabase_url),
                settings.supabase_service_key.get_secret_value()
            )
    result = client.table("users").delete().eq("email", email).execute()
    return len(result.data) if result.data else 0

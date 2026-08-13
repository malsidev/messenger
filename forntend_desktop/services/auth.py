from api.client import ApiClient
from services.token_storage import TokenStorage


class AuthService:

    def __init__(self, api: ApiClient, token_storage: TokenStorage):
        self.api = api
        self.token_storage = token_storage

    def login(self, username: str, password: str):
        print(f"[AuthService] Попытка входа для пользователя: {username}")
        response = self.api.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token") or data.get("token")
            print(f"[AuthService] Получен ответ логина: {data}")
            if token:
                self.token_storage.save_token(token)
                print("[AuthService] Токен успешно сохранён")
            else:
                print("[AuthService] В ответе не найден токен")
        else:
            print(f"[AuthService] Ошибка входа: {response.status_code} {response.text}")

        return response
from typing import Optional


class TokenStorage:
    """Хранит access token в памяти приложения."""

    def __init__(self):
        self._token: Optional[str] = None
        print("[TokenStorage] Инициализировано пустое хранилище токена")

    def save_token(self, token: str) -> None:
        self._token = token
        print(f"[TokenStorage] Токен сохранён: {token[:20]}...")

    def get_token(self) -> Optional[str]:
        print(f"[TokenStorage] Запрос токена из хранилища: {'есть' if self._token else 'нет'}")
        return self._token

    def clear(self) -> None:
        self._token = None
        print("[TokenStorage] Токен очищен")

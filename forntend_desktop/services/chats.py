from api.client import ApiClient


class ChatService:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.current_user_name = None

    def is_own_message(self, message: dict) -> bool:
        if message.get("is_me") is True or message.get("mine") is True or message.get("is_current_user") is True:
            return True

        sender = (
            message.get("sender")
            or message.get("username")
            or message.get("user")
            or message.get("from_user")
            or ""
        )
        if isinstance(sender, dict):
            sender = sender.get("username") or sender.get("name") or ""

        if self.current_user_name and sender:
            return str(sender).strip().lower() == str(self.current_user_name).strip().lower()

        if message.get("sender_id") is not None and message.get("sender_id") == message.get("current_user_id"):
            return True

        return False

    def get_chats(self):
        print("[ChatService] Отправляю GET /chats/")
        response = self.api_client.get("http://127.0.0.1:8001/chats/")

        if response.status_code == 200:
            chats = response.json()
            print(f"[ChatService] Получен список чатов: {chats}")
            return chats

        print(f"[ChatService] Ошибка получения чатов: {response.status_code} {response.text}")
        return []

    def get_messages(self, public_id: str):
        if not public_id:
            return []

        url = f"http://127.0.0.1:8001/chats/{public_id}/messages"
        print(f"[ChatService] Отправляю GET {url}")
        response = self.api_client.get(url)

        if response.status_code == 200:
            messages = response.json()
            print(f"[ChatService] Получены сообщения: {messages}")
            return messages

        print(f"[ChatService] Ошибка получения сообщений: {response.status_code} {response.text}")
        return []

import httpx

from services.token_storage import TokenStorage


class ApiClient:

    def __init__(self, token_storage: TokenStorage):
        self.token_storage = token_storage
        self.client = httpx.Client(
            base_url="http://localhost:8000",
            timeout=10.0,
        )

    def _get_auth_headers(self) -> dict:
        token = self.token_storage.get_token()
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            print(f"[ApiClient] Добавлен header Authorization для запроса: {headers['Authorization'][:20]}...")
            return headers

        print("[ApiClient] Токен отсутствует, Authorization не добавлен")
        return {}

    def get(self, url: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._get_auth_headers(), **headers}
        print(f"[ApiClient] GET {url}")
        response = self.client.get(url, headers=headers, **kwargs)
        print(f"[ApiClient] GET ответ: status={response.status_code}, body={response.text}")
        return response

    def post(self, url: str, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._get_auth_headers(), **headers}
        print(f"[ApiClient] POST {url} with json={kwargs.get('json')}" )
        response = self.client.post(url, headers=headers, **kwargs)
        print(f"[ApiClient] POST ответ: status={response.status_code}, body={response.text}")
        return response
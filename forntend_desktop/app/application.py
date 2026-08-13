import sys

from PyQt6.QtWidgets import QApplication
from app.window_manager import WindowManager
from api.client import ApiClient
from controllers.login_controller import LoginController
from services.auth import AuthService
from services.chats import ChatService
from services.token_storage import TokenStorage
from ui.login.login_window import LoginWindow
from ui.main.main_window import MainWindow


class Application:

    def __init__(self):
        self.qt_app = QApplication(sys.argv)

        with open("styles/dark.qss", "r") as file:
            self.qt_app.setStyleSheet(file.read())

        self.token_storage = TokenStorage()
        self.api_client = ApiClient(self.token_storage)
        self.auth_service = AuthService(self.api_client, self.token_storage)
        self.chat_service = ChatService(self.api_client)
        self.window_manager = WindowManager()
        self.login_controller = LoginController(self.auth_service)
        self.login_window = LoginWindow(self.login_controller)
        self.window_manager.main_window = MainWindow(self.chat_service)


        self.window_manager.login_window = self.login_window
        self.login_controller.login_success.connect(self.on_login_success)

    def on_login_success(self, username: str):
        self.chat_service.current_user_name = username
        self.window_manager.show_main()
        if self.window_manager.main_window and hasattr(self.window_manager.main_window, "chat_list"):
            self.window_manager.main_window.chat_list.load_chats()

    def run(self):
        self.window_manager.show_login()
        sys.exit(self.qt_app.exec())


def create_app():
    return Application()
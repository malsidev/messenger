from PyQt6.QtCore import QObject, pyqtSignal


class LoginController(QObject):

    login_success = pyqtSignal(str)

    def __init__(self, auth_service):
        super().__init__()

        self.auth_service = auth_service

    def login(self, username, password):

        response = self.auth_service.login(
            username,
            password,
        )

        if response.status_code == 200:
            self.login_success.emit(username)
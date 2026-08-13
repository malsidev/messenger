from ui.login.login_window import LoginWindow
from ui.main.main_window import MainWindow


class WindowManager:

    def __init__(self):
        self.login_window: LoginWindow | None = None
        self.main_window: MainWindow | None = None

    def show_login(self):
        self.login_window.show()

    def show_main(self):
        self.login_window.close()

        self.main_window.show()
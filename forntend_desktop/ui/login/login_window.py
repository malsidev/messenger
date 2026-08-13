from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

class LoginWindow(QWidget):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.setWindowTitle("Messenger")
        self.resize(400,300)

        self.init_ui()

    def init_ui(self):
                # Заголовок
        title = QLabel("Вход в Messenger")

        # Поле логина
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")

        # Поле пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопка
        self.login_button = QPushButton("Войти")

        # Вертикальное расположение элементов
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)

    def login(self):
        self.controller.login(
            self.login_input.text(),
            self.password_input.text(),
    )
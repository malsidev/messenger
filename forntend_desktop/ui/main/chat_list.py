from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLineEdit
)


class ChatList(QWidget):

    def __init__(self, chat_service=None, chat_widget=None):
        super().__init__()

        self.chat_service = chat_service
        self.chat_widget = chat_widget

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        self.chats = QListWidget()
        self.chats.itemClicked.connect(self.on_chat_clicked)

        layout.addWidget(self.search)
        layout.addWidget(self.chats)

        self.setLayout(layout)

    def load_chats(self):
        if not self.chat_service:
            self.chats.addItem("Нет сервиса чатов")
            return

        chats = self.chat_service.get_chats()
        self.chats.clear()

        self.chat_data = chats or []

        for chat in chats:
            title = chat.get("title", "Без названия")
            self.chats.addItem(title)

    def on_chat_clicked(self, item):
        for chat in self.chat_data:
            if chat.get("title") == item.text():
                public_id = chat.get("id")
                if self.chat_widget and public_id:
                    self.chat_widget.load_messages(public_id)
                break

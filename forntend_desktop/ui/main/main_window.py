from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter
)

from ui.main.chat_list import ChatList
from ui.main.chat_widget import ChatWidget


class MainWindow(QMainWindow):

    def __init__(self, chat_service=None):
        super().__init__()

        self.setWindowTitle("Messenger")
        self.resize(1200,700)


        splitter = QSplitter()
        splitter.setHandleWidth(6)


        # левая часть
        self.chat_widget = ChatWidget(chat_service)
        self.chat_list = ChatList(chat_service, self.chat_widget)


        splitter.addWidget(
            self.chat_list
        )

        splitter.addWidget(
            self.chat_widget
        )


        # размер панели
        splitter.setSizes(
            [300,900]
        )


        self.setCentralWidget(
            splitter
        )
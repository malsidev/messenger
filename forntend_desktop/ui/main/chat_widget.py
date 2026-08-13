from datetime import datetime

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QLabel,
    QSizePolicy,
)


class ChatWidget(QWidget):

    def __init__(self, chat_service=None):
        super().__init__()

        self.chat_service = chat_service

        main_layout = QVBoxLayout()

        self.messages = QScrollArea()
        self.messages.setWidgetResizable(True)
        self.messages.setFrameShape(QFrame.Shape.NoFrame)
        self.messages.setStyleSheet(
            "QScrollArea { background: #1f1f1f; border: none; }"
        )

        self.messages_content = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_content)
        self.messages_layout.setContentsMargins(6, 6, 6, 6)
        self.messages_layout.setSpacing(8)
        self.messages_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages.setWidget(self.messages_content)

        bottom = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Сообщение...")

        self.send = QPushButton("➤")

        bottom.addWidget(self.input)
        bottom.addWidget(self.send)

        main_layout.addWidget(self.messages)
        main_layout.addLayout(bottom)

        self.setLayout(main_layout)

    def load_messages(self, public_id: str):
        self._clear_messages()

        if not self.chat_service:
            self._add_empty_state("Нет сервиса сообщений")
            return

        messages = self.chat_service.get_messages(public_id)

        if not messages:
            self._add_empty_state("Нет сообщений")
            return

        for message in messages:
            text = message.get("text") or message.get("content") or ""
            timestamp = message.get("created_at") or message.get("timestamp") or message.get("time") or message.get("sent_at") or ""
            formatted_time = self._format_time(timestamp)
            is_own = self.chat_service.is_own_message(message) if self.chat_service else False
            self._add_message_bubble(text, formatted_time, is_own)

    def _clear_messages(self):
        while self.messages_layout.count():
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _add_empty_state(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #bdbdbd; padding: 12px;")
        self.messages_layout.addWidget(label)

    def _add_message_bubble(self, text: str, timestamp: str, is_own: bool):
        bubble = QFrame()
        bubble.setObjectName("messageBubble")
        bubble.setStyleSheet(
            "QFrame#messageBubble { border-radius: 16px; padding: 10px 12px; }"
            "QFrame#messageBubble { background-color: #3a3a3a; color: #f2f2f2; }"
            if not is_own else
            "QFrame#messageBubble { background-color: #2f80ed; color: white; }"
        )
        bubble.setMaximumWidth(430)
        bubble.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(10, 8, 10, 8)
        bubble_layout.setSpacing(4)

        content_label = QLabel(text)
        content_label.setWordWrap(True)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        content_label.setStyleSheet("color: inherit; background: transparent;")
        content_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop if is_own else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        bubble_layout.addWidget(content_label)

        if timestamp:
            time_label = QLabel(timestamp)
            time_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 10px; background: transparent;")
            time_label.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop if is_own else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
            )
            bubble_layout.addWidget(time_label)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        if is_own:
            row.addStretch()
            row.addWidget(bubble)
        else:
            row.addWidget(bubble)
            row.addStretch()

        self.messages_layout.addLayout(row)

    def _format_time(self, timestamp: str) -> str:
        if not timestamp:
            return ""

        try:
            if isinstance(timestamp, str):
                normalized = timestamp.replace("Z", "+00:00")
                dt = datetime.fromisoformat(normalized)
                return dt.strftime("%H:%M")
        except Exception:
            pass

        return str(timestamp)
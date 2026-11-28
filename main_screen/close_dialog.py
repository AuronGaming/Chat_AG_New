"""Диалог при закрытии окна"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox
from PyQt6.QtCore import Qt
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager
from main_screen.checkbox_style import checkbox_style

self.cb_remember.setStyleSheet(checkbox_style())


class CloseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Что сделать при закрытии?")
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        # Загружаем сохранённый выбор
        s = SettingsManager()
        self.saved_choice = s.settings.get("close_action", "ask")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(15)

        title = QLabel("Что сделать при закрытии?")
        title.setStyleSheet(f"font-size: 16px; color: {COLORS['accent']}; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)

        self.btn_minimize = QPushButton("📦 Свернуть в трей")
        self.btn_minimize.setStyleSheet(self._button_style())
        self.btn_minimize.clicked.connect(lambda: self._on_choice("minimize"))
        lay.addWidget(self.btn_minimize)

        self.btn_close = QPushButton("🚪 Закрыть полностью")
        self.btn_close.setStyleSheet(self._button_style())
        self.btn_close.clicked.connect(lambda: self._on_choice("exit"))
        lay.addWidget(self.btn_close)

        # Чекбокс "Запомнить мой выбор"
        self.cb_remember = QCheckBox("Запомнить мой выбор")
        self.cb_remember.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_primary']};
                font-size: 12px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px; height: 16px;
                border: 2px solid {COLORS['border']};
                border-radius: 3px;
                background-color: {COLORS['bg_input']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['accent']};
                border-color: {COLORS['accent']};
            }}
        """)
        lay.addWidget(self.cb_remember)

        self._choice = None

    def _button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent']};
                color: white;
                border-color: {COLORS['accent']};
            }}
        """

    def _on_choice(self, choice: str):
        """Сохранить выбор"""
        self._choice = choice

        # Если чекбокс отмечен — сохраняем в настройки
        if self.cb_remember.isChecked():
            s = SettingsManager()
            s.settings["close_action"] = choice
            s.save()
            print(f"💾 Запомнили выбор: {choice}")

        self.accept()

    def get_choice(self) -> str:
        return self._choice or "ask"
"""Панель активации — ник и ключ"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from main_screen.theme_config import COLORS, checkbox_style, input_style, green_button_style
from core.settings_manager import SettingsManager


class ActivationPanel(QWidget):
    """Настройки активации: ник + ключ (24 знака)"""

    activation_requested = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 10)
        lay.setSpacing(12)

        title = QLabel("🔑 Активация")
        title.setStyleSheet(f"font-size: 20px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        s = SettingsManager()
        other = s.settings.get("other", {})

        # Ник
        nick_row = QHBoxLayout()
        lbl_nick = QLabel("Ник:")
        lbl_nick.setFixedWidth(120)
        lbl_nick.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        nick_row.addWidget(lbl_nick)

        self.input_nick = QLineEdit()
        self.input_nick.setText(other.get("activation_nick", ""))
        self.input_nick.setPlaceholderText("Введите ник...")
        self.input_nick.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_nick.setStyleSheet(input_style())
        nick_row.addWidget(self.input_nick, stretch=1)

        self.cb_show_nick = QCheckBox("👁")
        self.cb_show_nick.setStyleSheet(checkbox_style())
        self.cb_show_nick.toggled.connect(lambda checked: self.input_nick.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        ))
        nick_row.addWidget(self.cb_show_nick)
        lay.addLayout(nick_row)

        # Ключ (24 знака)
        key_row = QHBoxLayout()
        lbl_key = QLabel("Ключ:")
        lbl_key.setFixedWidth(120)
        lbl_key.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        key_row.addWidget(lbl_key)

        self.input_key = QLineEdit()
        self.input_key.setText(other.get("activation_key", ""))
        self.input_key.setPlaceholderText("Введите ключ (24 знака)...")
        self.input_key.setMaxLength(24)
        self.input_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_key.setStyleSheet(input_style())
        key_row.addWidget(self.input_key, stretch=1)

        self.cb_show_key = QCheckBox("👁")
        self.cb_show_key.setStyleSheet(checkbox_style())
        self.cb_show_key.toggled.connect(lambda checked: self.input_key.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        ))
        key_row.addWidget(self.cb_show_key)
        lay.addLayout(key_row)

        # Кнопка Активировать
        btn_activate = QPushButton("🔑 Активировать")
        btn_activate.setFixedHeight(40)
        btn_activate.setStyleSheet(green_button_style(height=40))
        btn_activate.clicked.connect(self._on_activate)
        lay.addWidget(btn_activate)

        hint = QLabel("💡 Ник и ключ используются для активации лицензии")
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic;")
        lay.addWidget(hint)

        lay.addStretch()

    def _on_activate(self):
        nick = self.input_nick.text().strip()
        key = self.input_key.text().strip()
        if nick and key:
            self.activation_requested.emit(nick, key)
            print(f"🔑 Запрос активации: {nick}")
        else:
            print("⚠️ Заполните ник и ключ")

    def load_data(self, config: dict):
        self.input_nick.setText(config.get("activation_nick", ""))
        self.input_key.setText(config.get("activation_key", ""))

    def save_data(self) -> dict:
        return {
            "activation_nick": self.input_nick.text(),
            "activation_key": self.input_key.text(),
        }
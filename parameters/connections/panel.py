"""Панель настроек платформы"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager


class PlatformSettingsPanel(QWidget):
    """Настройки одной платформы"""

    connect_requested = pyqtSignal(str, dict)
    disconnect_requested = pyqtSignal(str)

    def __init__(self, platform_id: str, info: dict, parent=None):
        super().__init__(parent)
        self.platform_id = platform_id
        self.info = info
        self.field_widgets = {}
        self._build_ui()

    def _get_fields(self):
        if self.platform_id == 'youtube':
            return [
                ("API Key:", "api_key", "Введите API ключ...", True),
                ("Channel ID:", "channel_id", "UCxxxxxxxxxxxxxxxxxxxxxx", False),
            ]
        elif self.platform_id == 'vk_play':
            return [
                ("Логин:", "login", "Введите логин VK...", False),
                ("Пароль:", "password", "Введите пароль...", True),
                ("Channel ID:", "channel_id", "ID канала...", False),
            ]
        elif self.platform_id == 'donation_alerts':
            return [
                ("WebSocket Token:", "token", "Введите WebSocket токен...", True),
            ]
        elif self.platform_id == 'twitch':
            return [
                ("Никнейм:", "nickname", "Введите никнейм...", False),
                ("URL канала:", "channel", "https://www.twitch.tv/...", False),
                ("Токен (OAuth):", "token", "Введите токен...", True),
            ]
        else:
            return [
                ("Никнейм:", "nickname", "Введите никнейм...", False),
                ("URL канала:", "channel", "https://...", False),
                ("Токен:", "token", "Введите токен...", True),
            ]

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 10)
        lay.setSpacing(12)

        title = QLabel(self.info['name'])
        title.setStyleSheet(f"font-size: 20px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.btn_connect = QPushButton("🔗 Подключить")
        self.btn_connect.setFixedHeight(42)
        self.btn_connect.setStyleSheet(self._purple_button_style())
        self.btn_connect.clicked.connect(self._on_connect)
        top_row.addWidget(self.btn_connect)

        self.btn_get_token = QPushButton("🔑 Получить токен")
        self.btn_get_token.setFixedHeight(42)
        self.btn_get_token.setStyleSheet(self._purple_button_style())
        self.btn_get_token.clicked.connect(self._on_get_token)
        top_row.addWidget(self.btn_get_token)
        lay.addLayout(top_row)

        header_row = QHBoxLayout()
        self.cb_enabled = QCheckBox(f"Включить {self.info['name']}")
        self.cb_enabled.setStyleSheet(self._checkbox_style())
        header_row.addWidget(self.cb_enabled)
        header_row.addStretch()

        self.btn_logout = QPushButton("🗑 Разлогиниться")
        self.btn_logout.setFixedHeight(30)
        self.btn_logout.setStyleSheet(self._red_button_style())
        self.btn_logout.clicked.connect(lambda: self.disconnect_requested.emit(self.platform_id))
        header_row.addWidget(self.btn_logout)
        lay.addLayout(header_row)

        # Поля с кнопкой 👁 для паролей
        for label, key, placeholder, is_password in self._get_fields():
            row = QHBoxLayout()
            row.setSpacing(10)

            lbl = QLabel(label)
            lbl.setFixedWidth(120)
            lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
            row.addWidget(lbl)

            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            if is_password:
                inp.setEchoMode(QLineEdit.EchoMode.Password)
            inp.setStyleSheet(self._input_style())
            inp.setProperty("settings_key", key)
            row.addWidget(inp, stretch=1)
            self.field_widgets[key] = inp

            # Кнопка 👁 для полей с паролем/токеном
            if is_password:
                btn_show = QPushButton("👁")
                btn_show.setFixedWidth(30)
                btn_show.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['bg_input']};
                        color: {COLORS['text_primary']};
                        border: 1px solid {COLORS['border']};
                        border-radius: 4px;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {COLORS['bg_hover']};
                    }}
                """)
                btn_show.clicked.connect(lambda checked, w=inp: self._toggle_password_visibility(w))
                row.addWidget(btn_show)

            lay.addLayout(row)

        hint_text = f"💡 Нажмите 'Подключить' чтобы открыть {self.info['name']}."
        if self.info.get('token_url'):
            hint_text += f" Или 'Получить токен' для авторизации."
        hint = QLabel(hint_text)
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic; padding-top: 5px;")
        lay.addWidget(hint)

        lay.addStretch()

    def _toggle_password_visibility(self, widget: QLineEdit):
        """Переключить видимость пароля/токена"""
        if widget.echoMode() == QLineEdit.EchoMode.Password:
            widget.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            widget.setEchoMode(QLineEdit.EchoMode.Password)

    def _checkbox_style(self):
        return f"""
            QCheckBox {{
                color: {COLORS['text_primary']};
                font-size: 13px;
                font-weight: bold;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px; height: 16px;
                border: 2px solid {COLORS['accent']};
                border-radius: 3px;
                background-color: {COLORS['bg_input']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['accent']};
            }}
        """

    def _purple_button_style(self):
        return f"""
            QPushButton {{
                background-color: #8B5CF6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 16px;
            }}
            QPushButton:hover {{ background-color: #7C3AED; }}
        """

    def _red_button_style(self):
        return f"""
            QPushButton {{
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                padding: 4px 12px;
            }}
            QPushButton:hover {{ background-color: #dc2626; }}
        """

    def _input_style(self):
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
            }}
            QLineEdit:focus {{ border-color: {COLORS['accent']}; }}
        """

    def _on_connect(self):
        self.save_data()
        s = SettingsManager()
        config = s.settings.get("connections", {}).get(self.platform_id, {})
        config["enabled"] = True
        self.cb_enabled.setChecked(True)
        self.connect_requested.emit(self.platform_id, config)
        if self.info.get('connect_url'):
            QDesktopServices.openUrl(QUrl(self.info['connect_url']))

    def _on_get_token(self):
        if self.info.get('token_url'):
            QDesktopServices.openUrl(QUrl(self.info['token_url']))

    def load_data(self, config: dict):
        self.cb_enabled.setChecked(config.get("enabled", False))
        for key, widget in self.field_widgets.items():
            widget.setText(config.get(key, ""))

    def save_data(self):
        s = SettingsManager()
        connections = s.settings.get("connections", {})
        if self.platform_id not in connections:
            connections[self.platform_id] = {}
        connections[self.platform_id]["enabled"] = self.cb_enabled.isChecked()
        for key, widget in self.field_widgets.items():
            connections[self.platform_id][key] = widget.text()
        s.settings["connections"] = connections
        s.save()